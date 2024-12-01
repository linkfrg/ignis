from gi.repository import Gtk, GObject  # type: ignore
from ignis.base_widget import BaseWidget


class Box(Gtk.Box, BaseWidget):
    """
    Bases: :class:`Gtk.Box`.

    The main layout widget.

    .. hint::
        You can use generators to set children.

        .. code-block::

            Widget.Box(
                child=[Widget.Label(label=str(i)) for i in range(10)]
            )

    .. code-block:: python

        Widget.Box(
            child=[Widget.Label(label='heh'), Widget.Label(label='heh2')],
            vertical=False,
            homogeneous=False,
            spacing=52
        )
    """

    __gtype_name__ = "IgnisBox"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self)
        self._child: list[Gtk.Widget] = []
        BaseWidget.__init__(self, **kwargs)

    @GObject.Property
    def child(self) -> list[Gtk.Widget]:
        """
        - optional, read-write

        A list of child widgets.
        """
        return self._child

    @child.setter
    def child(self, child: list[Gtk.Widget]) -> None:
        for c in self._child:
            super().remove(c)

        self._child = []
        for c in child:
            if c:
                self.append(c)

    def append(self, child: Gtk.Widget) -> None:
        self._child.append(child)
        super().append(child)

    def remove(self, child: Gtk.Widget) -> None:
        self._child.remove(child)
        super().remove(child)

    def prepend(self, child: Gtk.Widget) -> None:
        self._child.insert(0, child)
        super().prepend(child)

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
