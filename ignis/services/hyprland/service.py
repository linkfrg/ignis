import json
import os
import socket
from gi.repository import GObject  # type: ignore
from ignis.utils import Utils
from ignis.exceptions import HyprlandIPCNotFoundError
from ignis.base_service import BaseService
from ignis.gobject import IgnisProperty
from .constants import HYPR_SOCKET_DIR
from .workspace import HyprlandWorkspace
from .keyboard import HyprlandKeyboard
from .window import HyprlandWindow


class HyprlandService(BaseService):
    """
    Hyprland IPC client.

    Example usage:

    .. code-block:: python

        from ignis.services.hyprland import HyprlandService

        hyprland = HyprlandService.get_default()

        # Get IDs of all workspaces
        print([i.id for i in hyprland.workspaces])

        # Get the ID of the active workspace
        print(hyprland.active_workspace.id)

        # Get the currently active keyboard layout
        print(hyprland.main_keyboard.active_keymap)

        # Get the title of the active window
        print(hyprland.active_window.title)
    """

    def __init__(self):
        super().__init__()

        self._workspaces: dict[int, HyprlandWorkspace] = {}
        self._active_workspace: HyprlandWorkspace = HyprlandWorkspace(self)
        self._main_keyboard: HyprlandKeyboard = HyprlandKeyboard(self)
        self._active_window: HyprlandWindow = HyprlandWindow()

        if self.is_available:
            self.__listen_events()

            self.__sync_workspaces()
            self.__sync_active_workspace()
            self.__sync_main_keyboard()
            self.__sync_active_window()

    @GObject.Signal(arg_types=(HyprlandWorkspace,))
    def workspace_added(self, *_):
        """
        - Signal

        Emitted when a new workspace has been added.

        Args:
            workspace (:class:`~ignis.services.hyprland.HyprlandWorkspace`): The instance of the workspace.
        """

    @IgnisProperty
    def is_available(self) -> bool:
        """
        - read-only

        Whether Hyprland IPC is available.
        """
        return os.path.exists(HYPR_SOCKET_DIR)

    @IgnisProperty
    def workspaces(self) -> list[HyprlandWorkspace]:
        """
        - read-only

        A list of workspaces.
        """
        return list(self._workspaces.values())

    @IgnisProperty
    def active_workspace(self) -> HyprlandWorkspace:
        """
        - read-only

        The currently active workspace.
        """
        return self._active_workspace

    @IgnisProperty
    def main_keyboard(self) -> HyprlandKeyboard:
        """
        - read-only

        The main keyboard.
        """
        return self._main_keyboard

    @IgnisProperty
    def active_window(self) -> HyprlandWindow:
        """
        - read-only

        The currenly focused window.
        """
        return self._active_window

    @Utils.run_in_thread
    def __listen_events(self) -> None:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect(f"{HYPR_SOCKET_DIR}/.socket2.sock")
            for event in Utils.listen_socket(sock, errors="ignore"):
                self.__on_event_received(event)

    def __on_event_received(self, event: str) -> None:
        event_data = event.split(">>")
        event_type = event_data[0]
        event_value = event_data[1]

        match event_type:
            case "destroyworkspace":
                self.__destroy_workspace(int(event_value))
            case "createworkspace":
                self.__create_workspace(int(event_value))
            case "workspace":
                self.__sync_active_workspace()
            case "focusedmon":
                self.__sync_active_workspace()
            case "activelayout":
                self.__sync_active_layout(event_value.split(",")[1])
            case "activewindow":
                self.__sync_active_window()
            case "renameworkspace":
                self.__sync_workspaces()

    def __create_workspace(self, id_: int) -> None:
        for i in json.loads(self.send_command("j/workspaces")):
            if id_ == i["id"]:
                workspace_data = i
                break
        else:
            workspace_data = None

        if workspace_data:
            workspace = HyprlandWorkspace(self)
            workspace._sync(workspace_data)
            self._workspaces[workspace_data["id"]] = workspace
            self.__sort_workspaces()
            self.emit("workspace-added", workspace)
            self.notify("workspaces")

    def __destroy_workspace(self, id_: int) -> None:
        workspace = self._workspaces.pop(int(id_), None)
        if workspace:
            workspace.emit("destroyed")
            self.__sort_workspaces()
            self.notify("workspaces")

    def __sort_workspaces(self) -> None:
        self._workspaces = dict(sorted(self._workspaces.items()))

    def __sync_workspaces(self) -> None:
        workspaces = sorted(
            json.loads(self.send_command("j/workspaces")), key=lambda x: x["id"]
        )
        for workspace_data in workspaces:
            workspace = self._workspaces.get(workspace_data["id"], None)
            if workspace is None:
                workspace = HyprlandWorkspace(self)

            workspace._sync(workspace_data)
            self._workspaces[workspace_data["id"]] = workspace

        self.__sort_workspaces()

        self.notify("workspaces")

    def __sync_active_workspace(self) -> None:
        workspace_data = json.loads(self.send_command("j/activeworkspace"))
        self._active_workspace._sync(workspace_data)
        self.notify("active-workspace")

    def __sync_main_keyboard(self) -> None:
        data_list = json.loads(self.send_command("j/devices"))["keyboards"]

        for kb_data in data_list:
            if kb_data["main"] is True:
                self._main_keyboard._sync(kb_data)

        self.notify("main-keyboard")

    def __sync_active_layout(self, layout: str) -> None:
        self._main_keyboard._sync({"active_keymap": layout})

    def __sync_active_window(self) -> None:
        active_window_data = json.loads(self.send_command("j/activewindow"))
        self.active_window._sync(active_window_data)
        self.notify("active-window")

    def send_command(self, cmd: str) -> str:
        """
        Send a command to the Hyprland IPC.
        Supports the same commands as ``hyprctl``.
        If you want to receive the response in JSON format, use this syntax: ``j/COMMAND``.

        Args:
            cmd: The command to send.

        Returns:
            Response from Hyprland IPC.

        Raises:
            HyprlandIPCNotFoundError: If Hyprland IPC is not found.
        """
        if not self.is_available:
            raise HyprlandIPCNotFoundError()

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect(f"{HYPR_SOCKET_DIR}/.socket.sock")
            return Utils.send_socket(sock, cmd, errors="ignore")

    def switch_to_workspace(self, workspace_id: int) -> None:
        """
        Switch to a workspace by its ID.

        Args:
            workspace_id: The ID of the workspace to switch to.
        """
        self.send_command(f"dispatch workspace {workspace_id}")

    def get_workspace_by_id(self, workspace_id: int) -> HyprlandWorkspace | None:
        """
        Get a workspace by its ID.

        Args:
            workspace_id: The ID of the workspace.
        Returns:
            The workspace instance, or ``None`` if the workspace with the given ID doesn't exist.
        """
        return self._workspaces.get(workspace_id, None)
