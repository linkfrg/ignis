import json
import os
import socket
from gi.repository import GObject  # type: ignore
from ignis.utils import Utils
from ignis.exceptions import NiriIPCNotFoundError
from ignis.base_service import BaseService
from ignis.gobject import IgnisProperty
from .constants import NIRI_SOCKET
from .keyboard import NiriKeyboardLayouts
from .output import NiriOutput
from .window import NiriWindow
from .workspace import NiriWorkspace


class NiriService(BaseService):
    """
    Niri IPC client.

    Example usage:

    .. code-block:: python

        from ignis.services.niri import NiriService

        niri = NiriService.get_default()

        # Get IDs of all workspaces
        print([i.id for i in niri.workspaces])

        # Get the ID of the active workspace on eDP-1
        print([i.id for i in niri.workspaces if i.is_active and i.output == "eDP-1"])

        # Get the currently active keyboard layout
        print(niri.keyboard_layouts.current_name)

        # Get the title of the active window
        print(niri.active_window.title)

        niri.connect("notify::kb-layout", lambda x, y: print(niri.kb_layout))
    """

    def __init__(self):
        super().__init__()

        self._keyboard_layouts: NiriKeyboardLayouts = NiriKeyboardLayouts(self)
        self._windows: dict[int, NiriWindow] = {}
        self._active_window: NiriWindow = NiriWindow(self)
        self._workspaces: dict[int, NiriWorkspace] = {}
        self._active_output: NiriOutput = NiriOutput()

        if self.is_available:
            self.__listen_events()
            # No need to send any commands after event stream initialization:
            #
            #  "The event stream IPC is designed to give you the complete current
            #  state up-front, then follow up with updates to that state. This way,
            #  your state can never "desync" from niri, and you don't need to make
            #  any other IPC information requests."
            #   - https://github.com/YaLTeR/niri/wiki/IPC

            # Except the state of outputs, which isn't streamed..
            self.__sync_active_output()

    @GObject.Signal()
    def workspace_added(self, workspace: NiriWorkspace):
        """
        - Signal

        Emitted when a new workspace has been added.

        Args:
            workspace: The instance of the workspace.
        """

    @IgnisProperty
    def is_available(self) -> bool:
        """
        - read-only

        Whether Niri IPC is available.
        """
        if NIRI_SOCKET is not None:
            return os.path.exists(NIRI_SOCKET)
        else:
            return False

    @IgnisProperty
    def keyboard_layouts(self) -> NiriKeyboardLayouts:
        """
        - read-only

        The currenly configured keyboard layouts.
        """
        return self._keyboard_layouts

    @IgnisProperty
    def windows(self) -> list[NiriWindow]:
        """
        - read-only

        A list of windows.
        """
        return list(self._windows.values())

    @IgnisProperty
    def active_window(self) -> NiriWindow:
        """
        - read-only

        The currenly focused window.
        """
        return self._active_window

    @IgnisProperty
    def workspaces(self) -> list[NiriWorkspace]:
        """
        - read-only

        A list of workspaces.
        """
        return list(self._workspaces.values())

    @IgnisProperty
    def active_output(self) -> NiriOutput:
        """
        - read-only

        The currenly focused output.
        """
        return self._active_output

    @Utils.run_in_thread
    def __listen_events(self) -> None:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect(str(NIRI_SOCKET))
            sock.send(b'"EventStream"\n')
            for event in Utils.listen_socket(sock, errors="ignore"):
                self.__on_event_received(event)

    def __on_event_received(self, event: str) -> None:
        json_data = json.loads(event)
        event_type = list(json_data.keys())[0]
        event_data = list(json_data.values())[0]
        match event_type:
            case "KeyboardLayoutSwitched":
                self.__update_current_layout(event_data)
            case "KeyboardLayoutsChanged":
                self.__update_keyboard_layouts(event_data)
            case "WindowClosed":
                self.__destroy_window(event_data)
            case "WindowFocusChanged":
                self.__update_window_focus(event_data)
            case "WindowOpenedOrChanged":
                self.__update_window(event_data)
            case "WindowsChanged":
                self.__update_windows(event_data)
            case "WorkspaceActivated":
                self.__update_active_workspace(event_data)
                self.__sync_active_output()
            case "WorkspaceActiveWindowChanged":
                self.__update_workspace_active_window(event_data)
            case "WorkspacesChanged":
                self.__update_workspaces(event_data)

    def __update_current_layout(self, data: dict) -> None:
        self._keyboard_layouts.sync({"current_idx": data["idx"]})
        self.notify("keyboard_layouts")
        self._keyboard_layouts.notify("current_name")

    def __update_keyboard_layouts(self, data: dict) -> None:
        self._keyboard_layouts.sync(data["keyboard_layouts"])
        self.notify("keyboard_layouts")
        self._keyboard_layouts.notify("current_name")

    def __sort_windows(self) -> None:
        self._windows = dict(sorted(self._windows.items()))

    def __destroy_window(self, data: dict) -> None:
        window = self._windows.pop(data["id"])
        if window:
            window.emit("destroyed")
            self.__sort_windows()
            self.notify("windows")

    def __update_window(self, data: dict) -> None:
        window_data = data["window"]
        window = self._windows.get(window_data["id"], None)
        if window is None:
            window = NiriWindow(self)

        window.sync(window_data)
        self._windows[window_data["id"]] = window

        if window.is_focused:
            self._active_window = window

        self.__sort_windows()

        self.notify("active-window")
        self.notify("windows")

    def __update_window_focus(self, data: dict) -> None:
        # Id of the newly focused window, or None if no window is now focused.
        id = data["id"]
        for _id, window in self._windows.items():
            # If a window became focused, it implies that all other windows
            # are no longer focused. Go through existing windows and
            # update their state accordingly.
            window.sync({"is_focused": (window.id == id)})

        if id:
            self._active_window = self._windows[id]
        else:
            self._active_window = NiriWindow(self)

        self.notify("active-window")
        self.notify("windows")

    def __update_windows(self, data: dict) -> None:
        windows = data["windows"]
        # WindowsChanged means a full replacement of window configuration.
        # Update every window accordingly.
        for window_data in windows:
            window = self._windows.get(window_data["id"], None)
            if window is None:
                window = NiriWindow(self)

            window.sync(window_data)
            self._windows[window_data["id"]] = window

            if window.is_focused:
                self._active_window = window

        # Drop windows that don't exist anymore.
        for id_, win in list(self._windows.items()):
            still_exists = False
            for window_data in windows:
                if window_data["id"] == id_:
                    still_exists = True
                    break

            if not still_exists:
                self._windows.pop(id_)
                win.emit("destroyed")

        self.__sort_windows()

        self.notify("active-window")
        self.notify("windows")

    def __sort_workspaces(self) -> None:
        self._workspaces = dict(
            sorted(self._workspaces.items(), key=lambda w: w[1].idx)
        )

    def __update_workspaces(self, data: dict) -> None:
        workspaces = data["workspaces"]
        # WorkspacesChanged means a full replacement of workspace configuration.
        # Update every workspace accordingly.
        for workspace_data in workspaces:
            workspace = self._workspaces.get(workspace_data["id"], None)
            if workspace is None:
                workspace = NiriWorkspace(self)

            workspace.sync(workspace_data)
            self._workspaces[workspace_data["id"]] = workspace

        # Drop workspaces that don't exist anymore.
        for id_, ws in list(self._workspaces.items()):
            still_exists = False
            for workspace_data in workspaces:
                if workspace_data["id"] == id_:
                    still_exists = True
                    break

            if not still_exists:
                self._workspaces.pop(ws.id)
                ws.emit("destroyed")

        self.__sort_workspaces()

        self.notify("workspaces")

    def __update_active_workspace(self, data: dict) -> None:
        id, focused = data["id"], data["focused"]
        output = self._workspaces[id].output
        for _id, workspace in self._workspaces.items():
            sync_data = {}
            # If a workspace became active, it implies that all other workspaces
            # on the same monitor became inactive. Go through existing workspaces
            # and update their state accordingly.
            got_activated = workspace.id == id
            if workspace.output == output:
                sync_data["is_active"] = got_activated
            if focused:
                sync_data["is_focused"] = got_activated
            workspace.sync(sync_data)

        self.notify("workspaces")

    def __update_workspace_active_window(self, data: dict) -> None:
        self._workspaces[data["workspace_id"]].sync(
            {"active_window_id": data["active_window_id"]}
        )

    def __sync_active_output(self) -> None:
        active_output_data = json.loads(self.send_command('"FocusedOutput"\n'))["Ok"][
            "FocusedOutput"
        ]
        self._active_output.sync(active_output_data)
        self.notify("active-output")

    def send_command(self, cmd: str) -> str:
        """
        Send a command to the Niri IPC.

        Args:
            cmd: The command to send.

        Returns:
            Response from Niri IPC.

        Raises:
            NiriIPCNotFoundError: If Niri IPC is not found.
        """
        if not self.is_available or NIRI_SOCKET is None:
            raise NiriIPCNotFoundError()

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect(NIRI_SOCKET)
            return Utils.send_socket(sock, cmd, errors="ignore")

    def switch_kb_layout(self) -> None:
        """
        Switch to the next keyboard layout.
        """
        self.send_command('{"Action":{"SwitchLayout":{"layout":"Next"}}}\n')

    def switch_to_workspace(self, workspace_id: int) -> None:
        """
        Switch to a workspace by its ID.

        Args:
            workspace_id: The ID of the workspace to switch to.
        """
        cmd = {"Action": {"FocusWorkspace": {"reference": {"Index": workspace_id}}}}
        self.send_command(json.dumps(cmd) + "\n")

    def get_workspace_by_id(self, workspace_id: int) -> NiriWorkspace | None:
        """
        Get a workspace by its ID.

        Args:
            workspace_id: The ID of the workspace.
        Returns:
            The workspace instance, or ``None`` if the workspace with the given ID doesn't exist.
        """
        return self._workspaces.get(workspace_id, None)
