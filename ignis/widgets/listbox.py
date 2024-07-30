from gi.repository import Gtk, GObject
from ignis.base_widget import BaseWidget
from typing import List
from ignis.widgets.listboxrow import ListBoxRow


class ListBox(Gtk.ListBox, BaseWidget):
    """
    Bases: `Gtk.ListBox <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/ListBox.html>`_.

    A vertical list that allows selecting rows. Well suited, for example, for a navigation bar.

    Properties:
        - **rows** (List[:class:`~ignis.widgets.listboxrow.ListBoxRow`], optional, read-write): List of rows.

    .. code-block:: python

        Widget.ListBox(
            rows=[
                Widget.ListBoxRow(label="row 1", on_activate=lambda x: print("selected row 1")),
                Widget.ListBoxRow(label="row 2", on_activate=lambda x: print("selected row 2"))
            ]
        )
    """

    __gtype_name__ = "IgnisListBox"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.ListBox.__init__(self)
        self._rows = []
        BaseWidget.__init__(self, **kwargs)

        self.connect("row_activated", self.__on_row_activated)

    def __on_row_activated(self, x, row):
        if isinstance(row, ListBoxRow):
            if row.on_activate:
                row.on_activate(row)

    def select_row(self, row: ListBoxRow) -> None:
        super().select_row(row)
        self.__on_row_activated(None, row)

    @GObject.Property
    def rows(self) -> List[ListBoxRow]:
        return self._rows

    @rows.setter
    def rows(self, value: List[ListBoxRow]) -> None:
        for i in self._rows:
            self.remove(i)

        for i in value:
            self.append(i)

            if isinstance(i, ListBoxRow):
                if i.selected:
                    self.select_row(i)

        self._rows = value
