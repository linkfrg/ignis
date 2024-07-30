from gi.repository import Gtk, GObject
from ignis.base_widget import BaseWidget
from typing import Any


class Switch(Gtk.Switch, BaseWidget):
    """
    Bases: `Gtk.Switch <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Switch.html>`_.

    A switch widget.

    Properties:
        - **on_change** (``callable``, optional, read-write): Function to call when the position of the switch changes (e.g., when the user toggles the switch).

    .. code-block:: python

        Widget.Switch(
            active=True,
            on_change=lambda x, active: print(active),
        )
    """

    __gtype_name__ = "IgnisSwitch"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.Switch.__init__(self)
        self._on_change = None
        self._can_activate = True
        BaseWidget.__init__(self, **kwargs)

        self.connect("state-set", self.__invoke_on_change)

    @GObject.Property
    def on_change(self) -> callable:
        return self._on_change

    @on_change.setter
    def on_change(self, value: callable) -> None:
        self._on_change = value

    def __invoke_on_change(self, *args) -> None:
        if self._can_activate and self.on_change:
            self.on_change(self, self.active)

    def set_property(self, property_name: str, value: Any) -> None:
        if property_name == "active":
            self._can_activate = False
            super().set_property(property_name, value)
            self._can_activate = True
        else:
            super().set_property(property_name, value)
