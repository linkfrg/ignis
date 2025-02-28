from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisProperty
from ._object import HyprlandObject

MATCH_DICT = {
    "monitorID": "monitor_id",
    "hasfullscreen": "has_fullscreen",
    "lastwindow": "last_window",
    "lastwindowtitle": "last_window_title",
}


class HyprlandWorkspace(HyprlandObject):
    """
    A workspace.
    """

    def __init__(self, service):
        super().__init__(match_dict=MATCH_DICT)
        self._service = service
        self._id: int = -1
        self._name: str = ""
        self._monitor: str = ""
        self._monitor_id: int = -1
        self._windows: int = -1
        self._has_fullscreen: bool = False
        self._last_window: str = ""
        self._last_window_title: str = ""

    @GObject.Signal
    def destroyed(self):
        """
        - Signal

        Emitted when the workspace has been destroyed.
        """

    @IgnisProperty
    def id(self) -> int:
        """
        - read-only

        The ID of the workspace.
        """
        return self._id

    @IgnisProperty
    def name(self) -> str:
        """
        - read-only

        The name of the workspace.
        """
        return self._name

    @IgnisProperty
    def monitor(self) -> str:
        """
        - read-only

        The monitor on which the workspace is placed.
        """
        return self._monitor

    @IgnisProperty
    def monitor_id(self) -> int:
        """
        - read-only

        The ID of the monitor on which the workspace is placed.
        """
        return self._monitor_id

    @IgnisProperty
    def windows(self) -> int:
        """
        - read-only

        The amount of windows on the workspace.
        """
        return self._windows

    @IgnisProperty
    def has_fullscreen(self) -> bool:
        """
        - read-only

        Whether the workspace has a fullscreen window.
        """
        return self._has_fullscreen

    @IgnisProperty
    def last_window(self) -> str:
        """
        - read-only

        The latest window.
        """
        return self._last_window

    @IgnisProperty
    def last_window_title(self) -> str:
        """
        - read-only

        The latest window title.
        """
        return self._last_window_title

    def switch_to(self) -> None:
        """
        Switch to this workspace.
        """
        self._service.send_command(f"dispatch workspace {self.id}")
