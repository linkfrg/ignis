from gi.repository import Gtk
from ignis.base_widget import BaseWidget

class HeaderBar(Gtk.HeaderBar, BaseWidget):
    """
    Bases: `Gtk.HeaderBar <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/HeaderBar.html>`_.

    A custom title bar with decorations like a close button and title.

    .. code-block:: python

        Widget.HeaderBar(
            show_title_buttons=True,
        )
    """

    __gtype_name__ = "IgnisHeaderBar"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.HeaderBar.__init__(self)
        BaseWidget.__init__(self, **kwargs)
