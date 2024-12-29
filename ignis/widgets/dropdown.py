from gi.repository import Gtk, GObject  # type: ignore
from ignis.base_widget import BaseWidget
from typing import Callable


class DropDown(Gtk.DropDown, BaseWidget):
    """
    Bases: :class:`Gtk.DropDown`

    A widget that allows the user to choose an item from a list of options.

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
        self._items: list[str] = []
        self._on_selected: Callable | None = None
        BaseWidget.__init__(self, **kwargs)

        self.connect("notify::selected-item", self.__invoke_on_selected)

    @GObject.Property
    def items(self) -> list[str]:
        """
        - optional, read-write

        A list of strings that can be selected in the popover.
        """
        return self._items

    @items.setter
    def items(self, value: list[str]) -> None:
        self._items = value
        model = Gtk.StringList()
        for i in value:
            model.append(i)

        self.model = model

    @GObject.Property
    def on_selected(self) -> Callable | None:
        """
        - optional, read-write

        The function to call when the user selects an item from the list.
        """
        return self._on_selected

    @on_selected.setter
    def on_selected(self, value: Callable) -> None:
        self._on_selected = value

    def __invoke_on_selected(self, *args) -> None:
        if self.on_selected:
            self.on_selected(self, self.selected)

    @GObject.Property
    def selected(self) -> str:
        """
        - not argument, read-only

        The selected string. It is a shortcut for ``self.selected_item.props.string``.
        """
        return self.selected_item.props.string
