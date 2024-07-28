from gi.repository import Gtk
from ignis.base_widget import BaseWidget


class Revealer(Gtk.Revealer, BaseWidget):
    """
    Bases: `Gtk.Revealer <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Revealer.html>`_.

    A container that animates the transition of its child from invisible to visible.

    Properties:
        - **transition_type** (``str``, optional, read-write): The type of transition. Possible values: ``"none"``, ``"crossfade"``, ``"slide_right"``, ``"slide_left"``, ``"slide_up"``, ``"slide_down"``.

    .. code-block:: python

        Widget.Revealer(
            child=Widget.Label(label='animation!!!'),
            transition_type='slideright',
            transition_duration=500,
            reveal_child=True, # Whether child is revealed.
        )
    """

    __gtype_name__ = "IgnisRevealer"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.Revealer.__init__(self)
        self.override_enum("transition_type", Gtk.RevealerTransitionType)
        BaseWidget.__init__(self, **kwargs)

    def toggle(self):
        if self.get_reveal_child():
            self.set_reveal_child(False)
        else:
            self.set_reveal_child(True)
