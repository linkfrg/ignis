from gi.repository import Gtk, GObject  # type: ignore
from ignis.base_widget import BaseWidget


class CenterBox(Gtk.CenterBox, BaseWidget):
    """
    Bases: :class:`Gtk.CenterBox`

    A box widget that contains three widgets, which are placed at the start, center, and end of the container.

    .. code-block:: python

        Widget.CenterBox(
            vertical=False,
            start_widget=Widget.Label(label='start'),
            center_widget=Widget.Label(label='center'),
            end_widget=Widget.Label(label='end'),
        )
    """

    __gtype_name__ = "IgnisCenterBox"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.CenterBox.__init__(self)
        BaseWidget.__init__(self, **kwargs)

    @GObject.Property
    def vertical(self) -> bool:
        """
        - optional, read-write

        Whether the box arranges children vertically.

        Default: ``False``.
        """
        return self.get_orientation() == Gtk.Orientation.VERTICAL

    @vertical.setter
    def vertical(self, value: bool) -> None:
        if value:
            self.set_property("orientation", Gtk.Orientation.VERTICAL)
        else:
            self.set_property("orientation", Gtk.Orientation.HORIZONTAL)
