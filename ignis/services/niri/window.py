import json
from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisProperty
from ._object import NiriObject


class NiriWindow(NiriObject):
    """
    A window.
    """

    def __init__(self, service):
        super().__init__()

        self._service = service
        self._id: int = -1
        self._title: str = ""
        self._app_id: str = ""
        self._pid: int = -1
        self._workspace_id: int = -1
        self._is_focused: bool = False
        self._is_floating: bool = False

    @GObject.Signal
    def destroyed(self):
        """
        - Signal

        Emitted when the window has been destroyed.
        """

    @IgnisProperty
    def id(self) -> int:
        """
        - read-only

        The unique ID of the window.
        """
        return self._id

    @IgnisProperty
    def title(self) -> str:
        """
        - read-only

        The title of the window.
        """
        return self._title

    @IgnisProperty
    def app_id(self) -> str:
        """
        - read-only

        Application ID of the window.
        """
        return self._app_id

    @IgnisProperty
    def pid(self) -> int:
        """
        - read-only

        The PID of the window.
        """
        return self._pid

    @IgnisProperty
    def workspace_id(self) -> int:
        """
        - read-only

        The ID of the workspace where the window is placed.
        """
        return self._workspace_id

    @IgnisProperty
    def is_focused(self) -> bool:
        """
        - read-only

        Whether the window is focused.
        """
        return self._is_focused

    @IgnisProperty
    def is_floating(self) -> bool:
        """
        - read-only

        Whether the window is floating.
        """
        return self._is_floating

    def close(self) -> None:
        """
        Close this window.
        """
        cmd = {"Action": {"CloseWindow": {"id": self._id}}}
        self._service.send_command(json.dumps(cmd) + "\n")
