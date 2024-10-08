from __future__ import annotations
from ignis.utils import Utils
from ignis.dbus import DBusProxy
from gi.repository import GLib, GObject, GdkPixbuf  # type: ignore
from ignis.gobject import IgnisGObject
from ignis.dbus_menu import DBusMenu


class SystemTrayItem(IgnisGObject):
    """
    System tray item.

    .. warning::
        If you want to add ``menu`` to several containers (e.g., make two status bars with a system tray),
        you must call the ``copy()`` method to obtain a copy of the menu.
        This is necessary because you can't add a single widget to multiple containers.

        .. code-block:: python

            menu = item.menu.copy()

    Signals:
        - **"removed"** (): Emitted when the item is removed.

    Properties:
        - **id** (``str``, read-only): The ID of the item.
        - **category** (``str``, read-only): The category of the item.
        - **title** (``str``, read-only): The title of the item.
        - **status** (``str``, read-only): The status of the item.
        - **window_id** (``int``, read-only): The window ID.
        - **icon** (``str | GdkPixbuf.Pixbuf | None``, read-only): The icon name or a ``GdkPixbuf.Pixbuf``.
        - **item_is_menu** (``bool``, read-only): Whether the item has a menu.
        - **menu** (``DBusMenu | None``, read-only): A :class:`~ignis.dbus_menu.DBusMenu` or ``None``. Add it to a container, and call the ``popup()`` method on it to display the menu.
        - **tooltip** (``str``, read-only): Tooltip, the text should be displayed when you hover cursor over the icon.

    """

    __gsignals__ = {
        "ready": (
            GObject.SignalFlags.RUN_FIRST,
            GObject.TYPE_NONE,
            (),
        ),  # user shouldn't connect to this signal
        "removed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, name: str, object_path: str):
        super().__init__()

        self._title: str | None = None
        self._icon: str | GdkPixbuf.Pixbuf | None = None
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

    @GObject.Property
    def id(self) -> str:
        return self.__dbus.Id

    @GObject.Property
    def category(self) -> str:
        return self.__dbus.Category

    @GObject.Property
    def title(self) -> str:
        return self.__dbus.Title

    @GObject.Property
    def status(self) -> str:
        return self.__dbus.Status

    @GObject.Property
    def window_id(self) -> int:
        return self.__dbus.WindowId

    @GObject.Property
    def icon(self) -> str | GdkPixbuf.Pixbuf | None:
        return self._icon

    @GObject.Property
    def item_is_menu(self) -> bool:
        return self.__dbus.ItemIsMenu

    @GObject.Property
    def menu(self) -> DBusMenu | None:
        return self._menu

    @GObject.Property
    def tooltip(self) -> str:
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
