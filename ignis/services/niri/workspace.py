from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisProperty, DataGObject


class NiriWorkspace(DataGObject):
    """
    A workspace.
    """

    def __init__(self, service):
        super().__init__()
        self._service = service
        self._id: int = -1
        self._idx: int = -1
        self._name: str = ""
        self._output: str = ""
        self._is_active: bool = False
        self._is_focused: bool = False
        self._active_window_id: int = -1

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

        The unique ID of the workspace.
        """
        return self._id

    @IgnisProperty
    def idx(self) -> int:
        """
        - read-only

        The index of the workspace on its monitor.
        """
        return self._idx

    @IgnisProperty
    def name(self) -> str:
        """
        - read-only

        The name of the workspace.
        """
        return self._name

    @IgnisProperty
    def output(self) -> str:
        """
        - read-only

        The name of the output on which the workspace is placed.
        """
        return self._output

    @IgnisProperty
    def is_active(self) -> bool:
        """
        - read-only

        Whether the workspace is currently active on its output.
        """
        return self._is_active

    @IgnisProperty
    def is_focused(self) -> bool:
        """
        - read-only

        Whether the workspace is currently focused.
        """
        return self._is_focused

    @IgnisProperty
    def active_window_id(self) -> int:
        """
        - read-only

        The ID of the active window on this workspace.
        """
        return self._active_window_id

    def switch_to(self) -> None:
        """
        Switch to this workspace.
        """
        cmd = {"Action": {"FocusWorkspace": {"reference": {"Index": self.id}}}}
        self._service.send_command(cmd)
