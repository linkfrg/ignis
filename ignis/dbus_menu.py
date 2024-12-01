from gi.repository import Gtk, Gio, GObject, GLib  # type: ignore
from ignis.dbus import DBusProxy
from ignis.app import IgnisApp
from ignis.utils import Utils

app = IgnisApp.get_default()


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
        action.connect("activate", self.__on_activate, item_id)
        app.add_action(action)

    @GObject.Property
    def uniq_name(self) -> str:
        return self._uniq_name

    def __on_activate(self, *args) -> None:
        self.__proxy.Event(
            "(isvu)",
            self._item_id,
            "clicked",
            GLib.Variant("i", 0),
            0,
            result_handler=lambda *args: None,
        )


class DBusMenu(Gtk.PopoverMenu):
    """
    Bases: :class:`Gtk.PopoverMenu`

    Like DbusmenuGtk3, but for GTK4.

    The bus must provide the ``com.canonical.dbusmenu`` D-Bus interface.
    """

    def __init__(self, name: str, object_path: str):
        super().__init__()
        self._name = name
        self._object_path = object_path

        self.__proxy = DBusProxy(
            name=name,
            object_path=object_path,
            interface_name="com.canonical.dbusmenu",
            info=Utils.load_interface_xml("com.canonical.dbusmenu"),
        )

        self.__proxy.signal_subscribe(
            "LayoutUpdated", lambda *args: self.__update_menu()
        )
        self.__proxy.signal_subscribe(
            "ItemsPropertiesUpdated", lambda *args: self.__update_menu()
        )

        self._menu_id: int = 0

        self.__update_menu()

    @GObject.Property
    def name(self) -> str:
        """
        - required, read-only

        A bus name (well-known or unique).
        """
        return self._name

    @GObject.Property
    def object_path(self) -> str:
        """
        - required, read-only

        An object path to the menu.
        """
        return self._object_path

    def __update_menu(self) -> None:
        self.__proxy.GetLayout(
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
            result_handler=self.__load_layout,
        )

    def __load_layout(self, proxy, result, user_data) -> None:
        if isinstance(result, GLib.GError):
            return

        self._menu_id = result[1][0]

        items = result[1][2]
        menu = self.__parse(items=items)
        self.set_menu_model(menu)

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
        return DBusMenu(self.__proxy.name, self.__proxy.object_path)

    def popup(self) -> None:
        try:
            self.__proxy.AboutToShow("(i)", self._menu_id)
        except GLib.GError:  # type: ignore
            pass
        return super().popup()
