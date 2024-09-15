from gi.repository import Gtk, GObject  # type: ignore
from ignis.base_widget import BaseWidget


class RegularWindow(Gtk.Window, BaseWidget):
    """
    Bases: `Gtk.Window <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Window.html>`_.

    A standart application window.

    Properties:
        - **namespace** (``str``, required, read-only): The name of the window, used for accessing it from the CLI and :class:`~ignis.app.ignisApp`. It must be unique.

    .. code-block:: python

        Widget.RegularWindow(
            child=Widget.Label(label="this is regular window"),
            title="This is title",
            namespace='some-regular-window',
            titlebar=Widget.HeaderBar(show_title_buttons=True),
        )
    """

    __gtype_name__ = "IgnisRegularWindow"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, namespace: str, **kwargs):
        Gtk.Window.__init__(self)
        BaseWidget.__init__(self, **kwargs)

        self._namespace = namespace

        from ignis.app import IgnisApp
        app = IgnisApp.get_default()

        app.add_window(namespace, self)

    @GObject.Property
    def namespace(self) -> str:
        return self._namespace
