from __future__ import annotations
from gi.repository import GObject, Gio, Gtk  # type: ignore
from ignis.gobject import IgnisGObject
from ignis.app import IgnisApp
from typing import Callable

app = IgnisApp.get_default()

class MenuItem(IgnisGObject):
    """
    Bases: :class:``ignis.gobject.IgnisGObject``.

    .. danger::
        This is not a regular widget.
        It doesn't support common widget properties and cannot be added as a child to a container.

    A class that represent a menu item.
    Intended for use in :class:`~ignis.widgets.Widget.PopoverMenu`.

    Properties:
        - **label** (``str``, required, read-only): The label of item.
        - **enabled** (``bool``, optional, read-only): Whether the item is enabled. If ``False``, the item cannot be selected.
        - **on_activate** (``Callable``, optional, read-write): Function to call when the user clicks on the item.
        - **submenu** (:class:`~ignis.widgets.Widget.PopoverMenu`, optional, read-only): The :class:`~ignis.widgets.Widget.PopoverMenu` that will appear when activated.

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
        submenu: Gtk.PopoverMenu | None = None,
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

    @GObject.Property
    def label(self) -> str:
        return self._label

    @GObject.Property
    def uniq_name(self) -> str:
        return self._uniq_name

    @GObject.Property
    def enabled(self) -> bool:
        return self._enabled

    @GObject.Property
    def on_activate(self) -> Callable:
        return self._on_activate

    @on_activate.setter
    def on_activate(self, value: Callable) -> None:
        self._on_activate = value

    def __on_activate(self, *args) -> None:
        self.on_activate(self)

    @GObject.Property
    def submenu(self) -> Gtk.PopoverMenu | None:
        return self._submenu
