from gi.repository import Gtk, GObject  # type: ignore
from ignis.base_widget import BaseWidget


class Separator(Gtk.Separator, BaseWidget):
    """
    Bases: :class:`Gtk.Separator`

    A separator widget.

    .. code-block:: python

        Widget.Separator(
            vertical=False,
        )
    """

    __gtype_name__ = "IgnisSeparator"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.Separator.__init__(self)
        BaseWidget.__init__(self, **kwargs)

    @GObject.Property
    def vertical(self) -> bool:
        """
        - optional, read-write

        Whether the separator is vertical.
        """
        return self.get_orientation() == Gtk.Orientation.VERTICAL

    @vertical.setter
    def vertical(self, value: bool) -> None:
        if value:
            self.set_property("orientation", Gtk.Orientation.VERTICAL)
        else:
            self.set_property("orientation", Gtk.Orientation.HORIZONTAL)
