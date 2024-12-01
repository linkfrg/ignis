from typing import Union, Literal
from ignis.utils import Utils
from ignis.dbus import DBusProxy
from gi.repository import GLib, GObject, GdkPixbuf  # type: ignore
from ignis.gobject import IgnisGObject
from ignis.dbus_menu import DBusMenu


class SystemTrayItem(IgnisGObject):
    """
    A system tray item.
    """

    def __init__(self, name: str, object_path: str):
        super().__init__()

        self._title: str | None = None
        self._icon: Union[str, GdkPixbuf.Pixbuf, None] = None
        self._tooltip: str | None = None
        self._status: str | None = None
        self._menu: DBusMenu | None = None

        self.__dbus: DBusProxy = DBusProxy(
            name=name,
            object_path=object_path,
            interface_name="org.kde.StatusNotifierItem",
            info=Utils.load_interface_xml("org.kde.StatusNotifierItem"),
        )

        if not self.__dbus.has_owner:
            return

        self.__dbus.proxy.connect(
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
                callback=lambda *args: Utils.thread(self.__sync_icon),
            )

        for signal_name in [
            "NewTitle",
            "NewToolTip",
            "NewStatus",
        ]:
            self.__dbus.signal_subscribe(
                signal_name=signal_name,
                callback=lambda *args, signal_name=signal_name: self.notify(
                    signal_name.replace("New", "").lower()
                ),
            )

        self.__ready()

    @Utils.run_in_thread
    def __ready(self) -> None:
        self.__sync_icon()
        self.emit("ready")

    def __sync_icon(self) -> None:
        icon_name = self.__dbus.IconName
        attention_icon_name = self.__dbus.AttentionIconName
        icon_pixmap = self.__dbus.IconPixmap
        attention_icon_pixmap = self.__dbus.AttentionIconPixmap

        if icon_name:
            self._icon = icon_name

        elif attention_icon_name:
            self._icon = attention_icon_name

        elif icon_pixmap:
            self._icon = self.__get_pixbuf(icon_pixmap)

        elif attention_icon_pixmap:
            self._icon = self.__get_pixbuf(attention_icon_pixmap)

        else:
            self._icon = "image-missing"

        self.notify("icon")

    @GObject.Signal
    def ready(self): ...  # user shouldn't connect to this signal

    @GObject.Signal
    def removed(self):
        """
        - Signal

        Emitted when the item is removed.
        """

    @GObject.Property
    def id(self) -> str:
        """
        - read-only

        The ID of the item.
        """
        return self.__dbus.Id

    @GObject.Property
    def category(self) -> str:
        """
        - read-only

        The category of the item.
        """
        return self.__dbus.Category

    @GObject.Property
    def title(self) -> str:
        """
        - read-only

        The title of the item.
        """
        return self.__dbus.Title

    @GObject.Property
    def status(self) -> str:
        """
        - read-only

        The status of the item.
        """
        return self.__dbus.Status

    @GObject.Property
    def window_id(self) -> int:
        """
        - read-only

        The window ID.
        """
        return self.__dbus.WindowId

    @GObject.Property
    def icon(self) -> Union[str, GdkPixbuf.Pixbuf, None]:
        """
        - read-only

        The icon name or a ``GdkPixbuf.Pixbuf``.
        """
        return self._icon

    @GObject.Property
    def item_is_menu(self) -> bool:
        """
        - read-only

        Whether the item has a menu.
        """
        return self.__dbus.ItemIsMenu

    @GObject.Property
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

    @GObject.Property
    def tooltip(self) -> str:
        """
        - read-only

        A tooltip, the text should be displayed when you hover cursor over the icon.
        """
        tooltip = self.__dbus.ToolTip
        return self.title if not tooltip else tooltip[2]

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
