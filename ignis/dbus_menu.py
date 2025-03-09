import asyncio
from gi.repository import Gtk, Gio, GObject, GLib  # type: ignore
from ignis.dbus import DBusProxy
from ignis.app import IgnisApp
from ignis.utils import Utils
from ignis.gobject import IgnisProperty

app = IgnisApp.get_default()


DBUS_GET_LAYOUT_ARGS = (
    "(iias)",
    0,
    -1,
    [
        "type",
        "children-display",
        "submenu",
        "type",
        "label",
        "visible",
        "enabled",
        "accessible-desc",
    ],
)


class MenuItem(GObject.Object):
    """
    :meta private:
    """

    def __init__(
        self,
        proxy: DBusProxy,
        item_id: int,
        enabled: bool = False,
    ):
        self.__proxy = proxy
        self._uniq_name = hex(id(self))
        self._item_id = item_id
        action = Gio.SimpleAction.new(self._uniq_name, None)
        action.set_enabled(enabled)
        action.connect("activate", lambda *_: asyncio.create_task(self.__on_activate()))
        app.add_action(action)

    @IgnisProperty
    def uniq_name(self) -> str:
        return self._uniq_name

    async def __on_activate(self) -> None:
        await self.__proxy.EventAsync(
            "(isvu)",
            self._item_id,
            "clicked",
            GLib.Variant("i", 0),
            0,
        )


class DBusMenu(Gtk.PopoverMenu):
    """
    Bases: :class:`Gtk.PopoverMenu`

    Like DbusmenuGtk3, but for GTK4.

    The bus must provide the ``com.canonical.dbusmenu`` D-Bus interface.
    """

    def __init__(self, proxy: DBusProxy):
        super().__init__()

        self.__proxy = proxy
        self._menu_id: int = 0

        self.__proxy.signal_subscribe(
            "LayoutUpdated", lambda *args: asyncio.create_task(self.__sync())
        )
        self.__proxy.signal_subscribe(
            "ItemsPropertiesUpdated",
            lambda *args: asyncio.create_task(self.__sync()),
        )

    @classmethod
    def new(cls, name: str, object_path: str) -> "DBusMenu":  # type: ignore
        """
        Synchronously initialize a new instance.

        Args:
            name: A bus name (well-known or unique).
            object_path: An object path to the menu.
        Returns:
            The newly initialized instance.
        """
        proxy = DBusProxy.new(
            name=name,
            object_path=object_path,
            interface_name="com.canonical.dbusmenu",
            info=Utils.load_interface_xml("com.canonical.dbusmenu"),
        )
        obj = cls(proxy)
        layout = proxy.GetLayout(*DBUS_GET_LAYOUT_ARGS)
        obj._update_menu(layout)
        return obj

    @classmethod
    async def new_async(cls, name: str, object_path: str) -> "DBusMenu":
        """
        Asynchronously initialize a new instance.

        Args:
            name: A bus name (well-known or unique).
            object_path: An object path to the menu.
        Returns:
            The newly initialized instance.
        """
        proxy = await DBusProxy.new_async(
            name=name,
            object_path=object_path,
            interface_name="com.canonical.dbusmenu",
            info=Utils.load_interface_xml("com.canonical.dbusmenu"),
        )
        obj = cls(proxy)
        layout = await proxy.GetLayoutAsync(*DBUS_GET_LAYOUT_ARGS)
        obj._update_menu(layout)
        return obj

    @IgnisProperty
    def name(self) -> str:
        """
        A bus name (well-known or unique).
        """
        return self.__proxy.name

    @IgnisProperty
    def object_path(self) -> str:
        """
        An object path to the menu.
        """
        return self.__proxy.object_path

    def _update_menu(self, layout: list) -> None:
        self._menu_id = layout[1][0]

        items = layout[1][2]
        menu = self.__parse(items=items)
        self.set_menu_model(menu)

    async def __sync(self) -> None:
        try:
            layout = await self.__proxy.GetLayoutAsync(*DBUS_GET_LAYOUT_ARGS)
        except GLib.Error:
            return

        if not layout:
            return

        self._update_menu(layout)

    def __parse(self, items: tuple) -> Gio.Menu:
        sections = []
        current_section = Gio.Menu()
        sections.append(current_section)
        for i in items:
            item_id = i[0]
            data_dict = i[1]
            child = i[2]

            visible = data_dict.get("visible", True)
            enabled = data_dict.get("enabled", True)
            label = data_dict.get("label", None)
            type = data_dict.get("type", None)

            if type == "separator":
                current_section = Gio.Menu()
                sections.append(current_section)
                continue

            if visible:
                item = MenuItem(proxy=self.__proxy, item_id=item_id, enabled=enabled)

                if child != []:
                    submenu = self.__parse(items=child)
                    current_section.append_submenu(label, submenu)
                else:
                    current_section.append(label, f"app.{item.uniq_name}")

        menu = Gio.Menu()
        for i in sections:
            menu.append_section(None, i)

        return menu

    def __copy__(self):
        return self.copy()

    def copy(self) -> "DBusMenu":
        """
        Create a copy of this instance.

        Returns:
            :class:`~ignis.dbus_menu.DBusMenu`: A copy of this instance.
        """
        return DBusMenu.new(self.__proxy.name, self.__proxy.object_path)

    async def copy_async(self) -> "DBusMenu":
        """
        Asynchronously create a copy of this instance.

        Returns:
            :class:`~ignis.dbus_menu.DBusMenu`: A copy of this instance.
        """
        return await DBusMenu.new_async(self.__proxy.name, self.__proxy.object_path)

    def popup(self) -> None:
        try:
            self.__proxy.AboutToShow("(i)", self._menu_id)
        except GLib.Error:
            pass
        return super().popup()
