from typing import Literal
from ignis.utils import Utils
from ignis.dbus import DBusProxy
from gi.repository import GLib, GObject, GdkPixbuf, Gtk, Gdk  # type: ignore
from ignis.gobject import IgnisGObject, IgnisProperty
from ignis.dbus_menu import DBusMenu
from ignis.exceptions import DisplayNotFoundError


class SystemTrayItem(IgnisGObject):
    """
    A system tray item.
    """

    def __init__(self, name: str, object_path: str):
        super().__init__()

        self._id: str | None = None
        self._category: str | None = None
        self._title: str | None = None
        self._status: str | None = None
        self._window_id: int = -1
        self._icon: str | GdkPixbuf.Pixbuf | None = None
        self._item_is_menu: bool = False
        self._menu: DBusMenu | None = None
        self._tooltip: str | None = None

        DBusProxy.new_async(
            name=name,
            object_path=object_path,
            interface_name="org.kde.StatusNotifierItem",
            info=Utils.load_interface_xml("org.kde.StatusNotifierItem"),
            callback=self.__on_proxy_initialized,
        )

    def __on_proxy_initialized(self, proxy: DBusProxy) -> None:
        self.__dbus = proxy

        if not self.__dbus.has_owner:
            return

        self.__dbus.gproxy.connect(
            "notify::g-name-owner", lambda *args: self.emit("removed")
        )

        menu_path: str = self.__dbus.Menu
        if menu_path:
            self._menu = DBusMenu(name=self.__dbus.name, object_path=menu_path)

        for signal_name in [
            "NewIcon",
            "NewAttentionIcon",
            "NewOverlayIcon",
        ]:
            self.__dbus.signal_subscribe(
                signal_name=signal_name,
                callback=lambda *args: self.__sync_icon(),
            )

        for signal_name in [
            "NewTitle",
            "NewToolTip",
            "NewStatus",
        ]:
            self.__dbus.signal_subscribe(
                signal_name=signal_name,
                callback=lambda *args, signal_name=signal_name: self.__sync_property(
                    signal_name.replace("New", "").lower()
                ),
            )

        display = Gdk.Display.get_default()
        if not display:
            raise DisplayNotFoundError()

        self._icon_theme = Gtk.IconTheme.get_for_display(display)
        self._icon_theme.connect("changed", lambda x: self.__sync_icon())

        # sync icon
        self.__sync_icon()

        # sync all properties
        self.__sync_property("id")
        self.__sync_property("category")
        self.__sync_property("title")
        self.__sync_property("status")
        self.__sync_property("window_id")
        self.__sync_property("item_is_menu")
        self.__sync_property("tooltip")

        self.emit("ready")

    def __sync_property(self, py_name: str) -> None:
        def callback(value):
            if isinstance(value, GLib.Error):
                return

            setattr(self, f"_{py_name}", value)
            self.notify(py_name.replace("_", "-"))

        self.__dbus.get_dbus_property_async(
            Utils.snake_to_pascal(py_name), callback=callback
        )

    def __sync_icon(self) -> None:
        def handle_icon_name(
            icon_name: str | None, icon_theme_path: str | None
        ) -> None:
            if icon_name and not isinstance(icon_name, GLib.Error):
                self._icon = icon_name
                search_path = self._icon_theme.get_search_path()
                if (
                    not self._icon_theme.has_icon(icon_name)
                    and icon_theme_path is not None
                    and search_path is not None
                    and icon_theme_path not in search_path
                ):
                    self._icon_theme.add_search_path(icon_theme_path)
                self.notify("icon")
            else:
                self.__dbus.get_dbus_property_async(
                    "AttentionIconName", handle_attention_icon_name, icon_theme_path
                )

        def handle_attention_icon_name(
            attention_icon_name: str | None, icon_theme_path: str | None
        ) -> None:
            if attention_icon_name and not isinstance(attention_icon_name, GLib.Error):
                self._icon = attention_icon_name
                search_path = self._icon_theme.get_search_path()
                if (
                    not self._icon_theme.has_icon(attention_icon_name)
                    and icon_theme_path is not None
                    and search_path is not None
                    and icon_theme_path not in search_path
                ):
                    self._icon_theme.add_search_path(icon_theme_path)
                self.notify("icon")
            else:
                self.__dbus.get_dbus_property_async("IconPixmap", handle_icon_pixmap)

        def handle_icon_pixmap(icon_pixmap) -> None:
            if icon_pixmap and not isinstance(icon_pixmap, GLib.Error):
                self._icon = self.__get_pixbuf(icon_pixmap)
                self.notify("icon")
            else:
                self.__dbus.get_dbus_property_async(
                    "AttentionIconPixmap", handle_attention_icon_pixmap
                )

        def handle_attention_icon_pixmap(attention_icon_pixmap) -> None:
            if attention_icon_pixmap and not isinstance(
                attention_icon_pixmap, GLib.Error
            ):
                self._icon = self.__get_pixbuf(attention_icon_pixmap)
                self.notify("icon")
            else:
                self._icon = "image-missing"
                self.notify("icon")

        def handle_icon_theme_path(icon_theme_path: str | None) -> None:
            self.__dbus.get_dbus_property_async(
                "IconName", handle_icon_name, icon_theme_path
            )

        self.__dbus.get_dbus_property_async("IconThemePath", handle_icon_theme_path)

    @GObject.Signal
    def ready(self): ...  # user shouldn't connect to this signal

    @GObject.Signal
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
