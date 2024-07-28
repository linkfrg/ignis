from gi.repository import Gtk, GObject
from ignis.base_widget import BaseWidget


class Entry(Gtk.Entry, BaseWidget):
    """
    Bases: `Gtk.Entry <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Entry.html>`_.

    An input field. To make it work, set the ``kb_mode`` property of the window to ``"on_demand"`` or ``"exclusive"``.

    Properies:
        - **on_accept** (``callable``, optional, read-write): The function that will be called when the user hits the Enter key.
        - **on_change** (``callable``, optional, read-write): The function that will be called when the text in the widget is changed (e.g., when the user types something into the entry).

    .. code-block:: python

        Widget.Entry(
            placeholder="placeholder",
            on_accept=lambda x: print(x.text),
            on_change=lambda x: print(x.text),
        )
    """
    __gtype_name__ = "IgnisEntry"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.Entry.__init__(self)
        self._on_accept = None
        self._on_change = None
        BaseWidget.__init__(self, **kwargs)

        self.connect("activate", lambda x: self.on_accept(x) if self.on_accept else None)
        self.connect(
            "notify::text", lambda x, y: self.on_change(x) if self.on_change else None
        )

    @GObject.Property
    def on_accept(self) -> callable:
        return self._on_accept

    @on_accept.setter
    def on_accept(self, value: callable) -> None:
        self._on_accept = value

    @GObject.Property
    def on_change(self) -> callable:
        return self._on_change

    @on_change.setter
    def on_change(self, value: callable) -> None:
        self._on_change = value
