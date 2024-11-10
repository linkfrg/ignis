from gi.repository import Gtk, GObject, Gio  # type: ignore
from ignis.base_widget import BaseWidget
from ignis.widgets.menuitem import MenuItem


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
        self._sections: list[Gio.Menu] = []
        self._menu = Gio.Menu()
        self._current_section = Gio.Menu()
        self._sections.append(self._current_section)

        BaseWidget.__init__(self, visible=False, **kwargs)

    def __add_item(self, item: MenuItem) -> None:
        self._items.append(item)

        if isinstance(item, Gtk.Separator):
            self._current_section = Gio.Menu()
            self._sections.append(self._current_section)
            return

        if item.submenu:
            self._current_section.append_submenu(item.label, item.submenu.menu_model)
        else:
            self._current_section.append(item.label, f"app.{item.uniq_name}")

        self._menu.remove_all()
        for i in self._sections:
            self._menu.append_section(None, i)

        self.set_menu_model(self._menu)

    @GObject.Property
    def items(self) -> list[MenuItem]:
        """
        - optional, read-write

        A list of :class:`~ignis.widgets.Widget.MenuItem`.
        """
        return self._items

    @items.setter
    def items(self, value: list[MenuItem]) -> None:
        self._menu = Gio.Menu()
        self.set_menu_model(self._menu)

        for item in value:
            self.__add_item(item)
