import asyncio
from typing import Literal
from collections.abc import Callable
from ignis.utils import Utils
from ignis.dbus import DBusProxy
from gi.repository import GLib, GdkPixbuf, Gtk, Gdk  # type: ignore
from ignis.gobject import IgnisGObject, IgnisProperty, IgnisSignal
from ignis.dbus_menu import DBusMenu
from ignis.exceptions import DisplayNotFoundError
from ignis.connection_manager import ConnectionManager, DBusConnectionManager


class SystemTrayItem(IgnisGObject):
    """
    A system tray item.
    """

    def __init__(self, name: str, object_path: str):
        super().__init__()

        self._conn_mgr = ConnectionManager()
        self._dbus_conn_mgr = DBusConnectionManager()

        self._id: str | None = None
        self._category: str | None = None
        self._title: str | None = None
        self._status: str | None = None
        self._window_id: int = -1
        self._icon: str | GdkPixbuf.Pixbuf | None = None
        self._item_is_menu: bool = False
        self._menu: DBusMenu | None = None
        self._tooltip: str | None = None

        asyncio.create_task(self.__init_proxy(name, object_path))

    async def __init_proxy(self, name: str, object_path: str) -> None:
        self.__dbus: DBusProxy = await DBusProxy.new_async(
            name=name,
            object_path=object_path,
            interface_name="org.kde.StatusNotifierItem",
            info=Utils.load_interface_xml("org.kde.StatusNotifierItem"),
        )

        if not self.__dbus.has_owner:
            return

        self._conn_mgr.connect(
            self.__dbus.gproxy, "notify::g-name-owner", lambda *_: self.__remove()
        )

        menu_path: str = await self.__dbus.get_dbus_property_async("Menu")

        if menu_path:
            self._menu = DBusMenu(name=self.__dbus.name, object_path=menu_path)

        for signal_name in [
            "NewIcon",
            "NewAttentionIcon",
            "NewOverlayIcon",
        ]:
            self._dbus_conn_mgr.subscribe(
                self.__dbus,
                signal_name,
                lambda *_: asyncio.create_task(self.__sync_icon()),
            )

        for signal_name in [
            "NewTitle",
            "NewToolTip",
            "NewStatus",
        ]:
            self._dbus_conn_mgr.subscribe(
                self.__dbus,
                signal_name,
                lambda *args, signal_name=signal_name: self.__sync_property(
                    signal_name.replace("New", "").lower()
                ),
            )

        display = Gdk.Display.get_default()
        if not display:
            raise DisplayNotFoundError()

        self._icon_theme = Gtk.IconTheme.get_for_display(display)
        self._conn_mgr.connect(
            self._icon_theme,
            "changed",
            lambda x: asyncio.create_task(self.__sync_icon()),
        )

        # sync icon
        await self.__sync_icon()

        # sync all properties
        await self.__sync_property("id")
        await self.__sync_property("category")
        await self.__sync_property("title")
        await self.__sync_property("status")
        await self.__sync_property("window_id")
        await self.__sync_property("item_is_menu")
        await self.__sync_property("tooltip")

        self.emit("ready")

    def __remove(self) -> None:
        self._conn_mgr.disconnect_all()
        self._dbus_conn_mgr.unsubscribe_all()
        self.emit("removed")

    async def __sync_property(self, py_name: str) -> None:
        try:
            value = await self.__dbus.get_dbus_property_async(
                Utils.snake_to_pascal(py_name)
            )
        except GLib.Error:
            return

        setattr(self, f"_{py_name}", value)
        self.notify(py_name.replace("_", "-"))

    async def __sync_icon(self) -> None:
        async def add_to_search_path(icon_name: str) -> None:
            search_path = self._icon_theme.get_search_path()
            try:
                icon_theme_path = await self.__dbus.get_dbus_property_async("IconName")
            except GLib.Error:
                return
            if (
                not self._icon_theme.has_icon(icon_name)
                and icon_theme_path is not None
                and search_path is not None
                and icon_theme_path not in search_path
            ):
                self._icon_theme.add_search_path(icon_theme_path)

        async def try_set_prop(
            property_name: str,
            callback: Callable | None = None,
            add_search_path: bool = False,
        ) -> bool:
            try:
                value = await self.__dbus.get_dbus_property_async(property_name)
            except GLib.Error:
                return False

            if value:
                if add_search_path:
                    await add_to_search_path(value)
                if callback:
                    self._icon = callback(value)
                else:
                    self._icon = value
                self.notify("icon")
                return True
            else:
                return False

        async def try_set_icon_name() -> None:
            is_success = await try_set_prop("IconName", add_search_path=True)
            if not is_success:
                await try_set_attention_icon_name()

        async def try_set_attention_icon_name() -> None:
            is_success = await try_set_prop("AttentionIconName", add_search_path=True)
            if not is_success:
                await try_set_icon_pixmap()

        async def try_set_icon_pixmap() -> None:
            is_success = await try_set_prop("IconPixmap", callback=self.__get_pixbuf)
            if not is_success:
                await try_set_attention_icon_pixmap()

        async def try_set_attention_icon_pixmap() -> None:
            is_success = await try_set_prop(
                "AttentionIconPixmap", callback=self.__get_pixbuf
            )
            if not is_success:
                self._icon = "image-missing"
                self.notify("icon")

        await try_set_icon_name()

    @IgnisSignal
    def ready(self): ...  # user shouldn't connect to this signal

    @IgnisSignal
    def removed(self):
        """
        - Signal

        Emitted when the item is removed.
        """

    @IgnisProperty
    def id(self) -> str | None:
        """
        - read-only

        The ID of the item.
        """
        return self._id

    @IgnisProperty
    def category(self) -> str | None:
        """
        - read-only

        The category of the item.
        """
        return self._category

    @IgnisProperty
    def title(self) -> str | None:
        """
        - read-only

        The title of the item.
        """
        return self._title

    @IgnisProperty
    def status(self) -> str | None:
        """
        - read-only

        The status of the item.
        """
        return self._status

    @IgnisProperty
    def window_id(self) -> int:
        """
        - read-only

        The window ID.
        """
        return self._window_id

    @IgnisProperty
    def icon(self) -> "str | GdkPixbuf.Pixbuf | None":
        """
        - read-only

        The icon name or a ``GdkPixbuf.Pixbuf``.
        """
        return self._icon

    @IgnisProperty
    def item_is_menu(self) -> bool:
        """
        - read-only

        Whether the item has a menu.
        """
        return self._item_is_menu

    @IgnisProperty
    def menu(self) -> DBusMenu | None:
        """
        - read-only

        A :class:`~ignis.dbus_menu.DBusMenu` or ``None``.

        .. hint::
            To display the menu, add it to a container, and call the ``.popup()`` method on it.

        .. warning::
            If you want to add ``menu`` to several containers (e.g., make two status bars with a system tray),
            you must call the ``copy()`` method to obtain a copy of the menu.
            This is necessary because you can't add a single widget to multiple containers.

            .. code-block:: python

                menu = item.menu.copy()
        """
        return self._menu

    @IgnisProperty
    def tooltip(self) -> str | None:
        """
        - read-only

        A tooltip, the text should be displayed when you hover cursor over the icon.
        """
        return self._title if not self._tooltip else self._tooltip[2]

    def __get_pixbuf(self, pixmap_array) -> GdkPixbuf.Pixbuf:
        pixmap = sorted(pixmap_array, key=lambda x: x[0])[-1]
        array = bytearray(pixmap[2])

        for i in range(0, 4 * pixmap[0] * pixmap[1], 4):
            alpha = array[i]
            array[i] = array[i + 1]
            array[i + 1] = array[i + 2]
            array[i + 2] = array[i + 3]
            array[i + 3] = alpha

        return GdkPixbuf.Pixbuf.new_from_bytes(
            GLib.Bytes.new(array),
            GdkPixbuf.Colorspace.RGB,
            True,
            8,
            pixmap[0],
            pixmap[1],
            pixmap[0] * 4,
        )

    def activate(self, x: int = 0, y: int = 0) -> None:
        """
        Activate the application.
        Usually this causes an application window to appear.

        Args:
            x: x coordinate.
            y: y coordinate.
        """
        self.__dbus.Activate("(ii)", x, y, result_handler=lambda *args: None)

    def secondary_activate(self, x: int = 0, y: int = 0) -> None:
        """
        Activate a secondary and less important action compared to :func:`activate`.

        Args:
            x: x coordinate.
            y: y coordinate.
        """
        self.__dbus.SecondaryActivate("(ii)", x, y, result_handler=lambda *args: None)

    def context_menu(self, x: int = 0, y: int = 0) -> None:
        """
        Ask the item to show a context menu.

        Args:
            x: x coordinate.
            y: y coordinate.
        """
        self.__dbus.ContextMenu("(ii)", x, y, result_handler=lambda *args: None)

    def scroll(
        self,
        delta: int = 0,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
    ) -> None:
        """
        Ask for a scroll action.

        Args:
            delta: The amount of scroll.
            orientation: The type of the orientation: horizontal or vertical.
        """
        self.__dbus.Scroll(
            "(is)", delta, orientation, result_handler=lambda *args: None
        )
