from gi.repository import Gtk
from ignis.base_widget import BaseWidget

class Scroll(Gtk.ScrolledWindow, BaseWidget):
    """
    Bases: `Gtk.ScrolledWindow <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/ScrolledWindow.html>`_.

    A container that accepts a single child widget and makes it scrollable.

    .. code-block:: python

        Widget.Scroll(
            child=Widget.Box(
                vertical=True,
                child=[Widget.Label(i) for i in range(30)]
            )
        )
    """
    __gtype_name__ = "IgnisScroll"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.ScrolledWindow.__init__(self)
        self.override_enum("hscrollbar_policy", Gtk.PolicyType)
        self.override_enum("vscrollbar_policy", Gtk.PolicyType)
        BaseWidget.__init__(self, **kwargs)
