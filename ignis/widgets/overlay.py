from gi.repository import Gtk, GObject  # type: ignore
from ignis.base_widget import BaseWidget


class Overlay(Gtk.Overlay, BaseWidget):
    """
    Bases: `Gtk.Overlay <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Overlay.html>`_.

    A container that places its children on top of each other.
    The ``child`` property is the main child, on which other widgets defined in ``overlays`` will be placed on top.

    Properties:
        - **overlays** (list[``Gtk.Widget``, optional, read-write]): A list of overlay widgets.

    .. code-block:: python

        Widget.Overlay(
            child=Widget.Label(label="This is the main child"),
            overlays=[
                Widget.Label(label="Overlay child 1"),
                Widget.Label(label="Overlay child 2"),
                Widget.Label(label="Overlay child 3"),
            ]
        )
    """

    __gtype_name__ = "IgnisOverlay"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.Overlay.__init__(self)
        self._overlays: list[Gtk.Widget] = []
        BaseWidget.__init__(self, **kwargs)

    @GObject.Property
    def overlays(self) -> list[Gtk.Widget]:
        return self._overlays

    @overlays.setter
    def overlays(self, value: list[Gtk.Widget]) -> None:
        for i in self._overlays:
            self.remove_overlay(i)

        self._overlays = value

        for i in value:
            self.add_overlay(i)
