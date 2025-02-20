from gi.repository import Gtk  # type: ignore
from ignis.base_widget import BaseWidget
from ignis.app import IgnisApp
from ignis.exceptions import WindowNotFoundError
from ignis.gobject import IgnisProperty

app = IgnisApp.get_default()


class RegularWindow(Gtk.Window, BaseWidget):
    """
    Bases: :class:`Gtk.Window`

    A standart application window.

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

        app.add_window(namespace, self)

        self.connect("close-request", self.__on_close_request)

    @IgnisProperty
    def namespace(self) -> str:
        """
        - required, read-only

        The name of the window, used for accessing it from the CLI and :class:`~ignis.app.IgnisApp`.
        It must be unique.
        """
        return self._namespace

    def __remove(self, *args) -> None:
        try:
            app.remove_window(self.namespace)
        except WindowNotFoundError:
            pass

    def __on_close_request(self, *args) -> None:
        if not self.props.hide_on_close:
            self.__remove()

    def destroy(self):
        self.__remove()
        return super().destroy()

    def unrealize(self):
        self.__remove()
        return super().unrealize()
