from gi.repository import Gtk, GObject  # type: ignore
from ignis.gobject import IgnisGObject


class StackPage(IgnisGObject):
    """
    Bases: :class:`~ignis.gobject.IgnisGObject`

    Intented to use with :class:`~ignis.widgets.Widget.Stack`.

    .. warning::
        It is not a widget.
    """

    def __init__(self, title: str, child: Gtk.Widget):
        super().__init__()
        self._title = title
        self._child = child

    @GObject.Property
    def title(self) -> str:
        """
        - required, read-only

        The title.
        It will be used by :class:`~ignis.widgets.Widget.StackSwitcher` to display :attr:`child` in a tab bar.
        """
        return self._title

    @GObject.Property
    def child(self) -> Gtk.Widget:
        """
        - required, read-only

        The child widget.
        """
        return self._child
