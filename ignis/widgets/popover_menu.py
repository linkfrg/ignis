from gi.repository import Gtk, Gio  # type: ignore
from ignis.base_widget import BaseWidget
from ignis.widgets.menuitem import MenuItem
from ignis.gobject import IgnisProperty


class PopoverMenu(Gtk.PopoverMenu, BaseWidget):
    """
    Bases: :class:`Gtk.PopoverMenu`

    A dropdown menu consisting of a list of :class:`~ignis.widgets.Widget.MenuItem`.
    It must be added as a child to a container.
    To display it, call the ``popup()`` method.

    .. code-block:: python

        Widget.PopoverMenu(
            items=[
                Widget.MenuItem(
                    label="Just item",
                    on_activate=lambda x: print("item activated!"),
                ),
                Widget.MenuItem(
                    label="This is disabled item",
                    enabled=False,
                    on_activate=lambda x: print("you will not see this message in terminal hehehehehe"),
                ),
                Widget.MenuItem(
                    label="This has submenu!",
                    on_activate=lambda x: print("anyway activate callback working"),
                    submenu=Widget.PopoverMenu(items=[Widget.MenuItem(label=str(i)) for i in range(10)])
                ),
            ]
        )
    """

    __gtype_name__ = "IgnisPopoverMenu"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.PopoverMenu.__init__(self)
        self._items: list[MenuItem] = []
        BaseWidget.__init__(self, visible=False, **kwargs)

    def __add_item(
        self, item: MenuItem, menu: Gio.Menu, current_section: Gio.Menu
    ) -> Gio.Menu:
        if isinstance(item, Gtk.Separator):
            current_section = Gio.Menu()
            menu.append_section(None, current_section)
            return current_section

        if item.submenu:
            current_section.append_submenu(item.label, item.submenu.menu_model)
        else:
            current_section.append(item.label, f"app.{item.uniq_name}")

        return current_section

    def __generate_menu(self, items: list[MenuItem]) -> Gio.Menu:
        menu = Gio.Menu.new()
        current_section = Gio.Menu()
        menu.append_section(None, current_section)

        for item in items:
            current_section = self.__add_item(item, menu, current_section)

        return menu

    @IgnisProperty
    def items(self) -> list[MenuItem]:
        """
        - optional, read-write

        A list of :class:`~ignis.widgets.Widget.MenuItem`.
        """
        return self._items

    @items.setter
    def items(self, value: list[MenuItem]) -> None:
        self._items = value
        self.set_menu_model(self.__generate_menu(items=value))
