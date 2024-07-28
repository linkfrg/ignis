from gi.repository import GObject, Gtk
from ignis.base_widget import BaseWidget

class ToggleButton(Gtk.ToggleButton, BaseWidget):
    """
    Bases: `Gtk.ToggleButton <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/ToggleButton.html>`_.

    A toggle button widget.

    Properties:
        - **on_toggled** (``callable``, optional, read-write): Function to call when the button is toggled by the user.

    .. code-block:: python

        Widget.ToggleButton(
            on_toggled=lambda x, active: print(active)
        )
        
    """

    __gtype_name__ = "IgnisToggleButton"
    __gproperties__ = {**BaseWidget.gproperties}
    
    def __init__(self, **kwargs) -> None:
        Gtk.ToggleButton.__init__(self)
        BaseWidget.__init__(self, **kwargs)

        self.connect("toggled", lambda x: self.on_toggled(self, self.active) if self.on_toggled else None)

    @GObject.Property
    def on_toggled(self) -> callable:
        return self._on_toggled
    
    @on_toggled.setter
    def on_toggled(self, value: callable) -> None:
        self._on_toggled = value