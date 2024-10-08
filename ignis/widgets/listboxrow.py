from gi.repository import Gtk, GObject  # type: ignore
from ignis.base_widget import BaseWidget
from typing import Callable


class ListBoxRow(Gtk.ListBoxRow, BaseWidget):
    """
    Bases: `Gtk.ListBoxRow <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/ListBoxRow.html>`_.

    A row for :class:`~ignis.widgets.listbox.ListBox`.

    Properties:
        - **on_activate** (``Callable``, optional, read-write): Function to call when the user selects the row.
        - **selected** (``bool``, optional, read-write): Whether the row is selected by default.

    .. code-block:: python

        Widget.ListBoxRow(
            label="row 1",
            on_activate=lambda x: print("selected row 1"),
            selected=True
        )
    """

    __gtype_name__ = "IgnisListBoxRow"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.ListBoxRow.__init__(self)
        self._on_activate: Callable | None = None
        self._selected: bool = False
        BaseWidget.__init__(self, **kwargs)

    @GObject.Property
    def on_activate(self) -> Callable:
        return self._on_activate

    @on_activate.setter
    def on_activate(self, value: Callable) -> None:
        self._on_activate = value

    @GObject.Property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        self._selected = value
