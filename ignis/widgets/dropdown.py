from gi.repository import Gtk, GObject
from ignis.base_widget import BaseWidget
from typing import List


class DropDown(Gtk.DropDown, BaseWidget):
    """
    Bases: `Gtk.DropDown <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/DropDown.html>`_.

    A widget that allows the user to choose an item from a list of options.

    Properties:
        - **items** (``List[str]``, optional, read-write): List of strings that can be selected in the popover.
        - **on_selected** (``callable``, optional, read-write): Function to call when the user selects an item from the list.
        - **selected** (``str``, read-only): The selected string. This is not an argument to the constructor; it is a shortcut for ``self.selected_item.props.string``.

    .. code-block:: python

        Widget.DropDown(
            items=["option 1", "option 2", "option 3"],
            on_selected=lambda x, selected: print(selected)
        )
    """

    __gtype_name__ = "IgnisDropDown"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.DropDown.__init__(self)
        self._items = []
        self._on_selected = None
        BaseWidget.__init__(self, **kwargs)

        self.connect("notify::selected-item", self.__invoke_on_selected)

    @GObject.Property
    def items(self) -> List[str]:
        return self._items

    @items.setter
    def items(self, value: List[str]) -> None:
        self._items = value
        model = Gtk.StringList()
        for i in value:
            model.append(i)

        self.model = model

    @GObject.Property
    def on_selected(self) -> callable:
        return self._on_selected

    @on_selected.setter
    def on_selected(self, value: callable) -> None:
        self._on_selected = value

    def __invoke_on_selected(self, *args) -> None:
        if self.on_selected:
            self.on_selected(self, self.selected)

    @GObject.Property
    def selected(self) -> str:
        return self.selected_item.props.string
