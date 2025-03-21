from gi.repository import Gio, Gtk  # type: ignore
from ignis.gobject import IgnisGObject
from ignis.app import IgnisApp
from collections.abc import Callable
from ignis.gobject import IgnisProperty

app = IgnisApp.get_default()


class MenuItem(IgnisGObject):
    """
    Bases: :class:`~ignis.gobject.IgnisGObject`

    .. danger::
        This is not a regular widget.
        It doesn't support common widget properties and cannot be added as a child to a container.

    A class that represent a menu item.
    Intended for use in :class:`~ignis.widgets.Widget.PopoverMenu`.

    Args:
        label: The label of item.
        enabled: Whether the item is enabled. If ``False``, the item cannot be selected.
        on_activate: The function to call when the user clicks on the item.
        submenu: The :class:`~ignis.widgets.Widget.PopoverMenu` that will appear when activated.

    .. code-block :: python

        Widget.MenuItem(
            label="item 1",
            enabled=True,
            on_activate=lambda x: print("menu item 1 activated!"),
            submenu=Widget.PopoverMenu()
        )
    """

    __gtype_name__ = "IgnisMenuItem"

    def __init__(
        self,
        label: str,
        enabled: bool = True,
        on_activate: Callable | None = None,
        submenu: "Gtk.PopoverMenu | None" = None,
    ):
        super().__init__()
        self._label = label
        self._enabled = enabled
        self._on_activate = on_activate
        self._submenu = submenu
        self._uniq_name = hex(id(self))

        action = Gio.SimpleAction.new(self._uniq_name, None)
        action.set_enabled(enabled)
        action.connect("activate", self.__on_activate)

        app.add_action(action)

    @IgnisProperty
    def label(self) -> str:
        """
        The label of item.
        """
        return self._label

    @IgnisProperty
    def uniq_name(self) -> str:
        """
        The unique name of the ``Gio.Action``.
        """
        return self._uniq_name

    @IgnisProperty
    def enabled(self) -> bool:
        """
        Whether the item is enabled. If ``False``, the item cannot be selected.
        """
        return self._enabled

    @IgnisProperty
    def on_activate(self) -> Callable:
        """
        The function to call when the user clicks on the item.
        """
        return self._on_activate

    @on_activate.setter
    def on_activate(self, value: Callable) -> None:
        self._on_activate = value

    def __on_activate(self, *args) -> None:
        self.on_activate(self)

    @IgnisProperty
    def submenu(self) -> "Gtk.PopoverMenu | None":
        """
        The :class:`~ignis.widgets.Widget.PopoverMenu` that will appear when activated.
        """
        return self._submenu
