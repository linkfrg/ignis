from ignis.utils import Utils
from ignis.dbus import DBusService, DBusProxy
from gi.repository import Gio, GLib, GObject, GdkPixbuf
from typing import Union
from ignis.gobject import IgnisGObject
from ignis.dbus_menu import DBusMenu
from ignis.logging import logger

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
        - **icon** (``Union[str, GdkPixbuf.Pixbuf]``, read-only): The icon name or a ``GdkPixbuf.Pixbuf``.
        - **item_is_menu** (``bool``, read-only): Whether the item has a menu.
        - **menu** (``DBusMenu``, read-only): A ``Gtk.PopoverMenu`` or ``None``. Add it to a container, and call the ``popup()`` method on it to display the menu.
        - **tooltip** (``str``, read-only): Tooltip, the text should be displayed when you hover cursor over the icon.

    """
    __gsignals__ = {
        "ready": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()), # user shouldn't connect to this signal
        "removed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, name: str, object_path: str):
        super().__init__()

        self._title = None
        self._icon = None
        self._tooltip = None
        self._status = None

        self.__dbus = DBusProxy(
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


        menu_path = self.__dbus.Menu
        if menu_path:
            self._menu = DBusMenu(name=self.__dbus.name, object_path=menu_path)
        else:
            self._menu = None

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
                callback=lambda *args: self.notify(signal_name.replace("New", "").lower()),
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
    def icon(self) -> Union[str, GdkPixbuf.Pixbuf]:
        return self._icon

    @GObject.Property
    def item_is_menu(self) -> bool:
        return self.__dbus.ItemIsMenu

    @GObject.Property
    def menu(self) -> DBusMenu:
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


class SystemTrayService(IgnisGObject):
    """
    A system tray, where application icons are placed.

    Signals:
        - **"added"** (:class:`~ignis.services.system_tray.SystemTrayItem`): Emitted when a new item is added.

    Properties:
        - **items** (List[:class:`~ignis.services.system_tray.SystemTrayItem`], read-only): A list of items.

    **Example usage:**

    .. code-block:: python

        from ignis.services import Service

        system_tray = Service.get("system_tray")

        system_tray.connect("added", lambda x, item: print(item.title))
        

    """
    __gsignals__ = {
        "added": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (GObject.Object,)),
    }

    def __init__(self):
        super().__init__()

        self.__dbus = DBusService(
            name="org.kde.StatusNotifierWatcher",
            object_path="/StatusNotifierWatcher",
            info=Utils.load_interface_xml("org.kde.StatusNotifierWatcher"),
            on_name_lost=lambda x, y: logger.error(
                "Another system tray is already running. Try to close other status bars/graphical shells."
            ),
        )

        self.__dbus.register_dbus_property(
            name="ProtocolVersion", method=self.__ProtocolVersion
        )
        self.__dbus.register_dbus_property(
            name="IsStatusNotifierHostRegistered",
            method=self.__IsStatusNotifierHostRegistered,
        )
        self.__dbus.register_dbus_property(
            name="RegisteredStatusNotifierItems",
            method=self.__RegisteredStatusNotifierItems,
        )

        self.__dbus.register_dbus_method(
            name="RegisterStatusNotifierItem", method=self.__RegisterStatusNotifierItem
        )

        self._items = {}

    @GObject.Property
    def items(self) -> list:
        return list(self._items.values())

    def __ProtocolVersion(self) -> GLib.Variant:
        return GLib.Variant("i", 0)

    def __IsStatusNotifierHostRegistered(self) -> GLib.Variant:
        return GLib.Variant("b", True)

    def __RegisteredStatusNotifierItems(self) -> GLib.Variant:
        return GLib.Variant("as", list(self._items.keys()))

    def __RegisterStatusNotifierItem(
        self, invocation: Gio.DBusMethodInvocation, service: str
    ) -> None:
        if service.startswith("/"):
            object_path = service
            bus_name = invocation.get_sender()

        else:
            object_path = "/StatusNotifierItem"
            bus_name = service

        invocation.return_value(None)

        item = SystemTrayItem(bus_name, object_path)
        item.connect("ready", self.__on_item_ready, bus_name, object_path)

    def __on_item_ready(
        self, item: SystemTrayItem, bus_name: str, object_path: str
    ) -> None:
        self._items[bus_name] = item
        item.connect("removed", self.__remove_item, bus_name)
        self.emit("added", item)
        self.notify("items")
        self.__dbus.emit_signal(
            "StatusNotifierItemRegistered",
            GLib.Variant("(s)", (bus_name + object_path,)),
        )

    def __remove_item(self, x, bus_name: str) -> None:
        self._items.pop(bus_name)
        self.notify("items")
        self.__dbus.emit_signal(
            "StatusNotifierItemUnregistered", GLib.Variant("(s)", (bus_name,))
        )
