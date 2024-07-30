from gi.repository import Gtk, GObject
from ignis.base_widget import BaseWidget


class CheckButton(Gtk.CheckButton, BaseWidget):
    """
    Bases: `Gtk.CheckButton <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/CheckButton.html>`_.

    A check button. If ``group`` is set, the check button behaves as a radio button.

    **Simple checkbutton:**

    .. code-block:: python

        Widget.CheckButton(
            label='check button',
            active=True,
        )

    **Radio button:**

    .. code-block:: python

        Widget.CheckButton(
            group=Widget.CheckButton(label='radiobutton 1'),
            label='radiobutton 2',
            active=True,
        )
    """

    __gtype_name__ = "IgnisCheckButton"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.CheckButton.__init__(self)
        BaseWidget.__init__(self, **kwargs)

        self.connect(
            "toggled",
            lambda x: self.on_toggled(x, x.active) if self.on_toggled else None,
        )

    @GObject.Property
    def on_toggled(self) -> callable:
        return self._on_toggled

    @on_toggled.setter
    def on_toggled(self, value: callable) -> None:
        self._on_toggled = value
