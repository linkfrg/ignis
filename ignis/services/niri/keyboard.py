import json
from ignis.gobject import IgnisProperty
from ._object import NiriObject


class NiriKeyboardLayouts(NiriObject):
    """
    Configured keyboard layouts.
    """

    def __init__(self, service):
        super().__init__()
        self._service = service
        self._names: list = []
        self._current_idx: int = -1
        self._main: bool = False

    @IgnisProperty
    def names(self) -> list:
        """
        - read-only

        XKB names of the configured layouts.
        """
        return self._names

    @IgnisProperty
    def current_idx(self) -> int:
        """
        - read-only

        Index of the currently active layout in names.
        """
        return self._current_idx

    def switch_layout(self, layout: str) -> None:
        """
        Switch the keyboard layout.

        Args:
            layout: The layout to switch to. Must be either: ``Next``, ``Prev``
            or a valid id (``0``, ``1``, etc.)
        """
        cmd = {"Action": {"SwitchLayout": {"layout": layout}}}
        self._service.send_command(json.dumps(cmd) + "\n")
