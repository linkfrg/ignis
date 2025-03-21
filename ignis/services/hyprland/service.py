import json
import os
import socket
from typing import Any
from ignis.utils import Utils
from ignis.exceptions import HyprlandIPCNotFoundError
from ignis.base_service import BaseService
from ignis.gobject import IgnisProperty, IgnisSignal
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
        self._windows: dict[str, HyprlandWindow] = {}
        self._active_window: HyprlandWindow = HyprlandWindow()

        if self.is_available:
            self.__listen_events()

            self.__initial_sync_workspaces()
            self.__sync_active_workspace()
            self.__sync_main_keyboard()
            self.__sync_active_window()
            self.__initial_sync_windows()

    @IgnisSignal
    def workspace_added(self, workspace: HyprlandWorkspace):
        """
        Emitted when a new workspace has been added.

        Args:
            workspace: The instance of the workspace.
        """

    @IgnisSignal
    def window_added(self, window: HyprlandWindow):
        """
        Emitted when a new window has been added.

        Args:
            window: The instance of the window.
        """

    @IgnisProperty
    def is_available(self) -> bool:
        """
        Whether Hyprland IPC is available.
        """
        return os.path.exists(HYPR_SOCKET_DIR)

    @IgnisProperty
    def workspaces(self) -> list[HyprlandWorkspace]:
        """
        A list of workspaces.
        """
        return list(self._workspaces.values())

    @IgnisProperty
    def active_workspace(self) -> HyprlandWorkspace:
        """
        The currently active workspace.
        """
        return self._active_workspace

    @IgnisProperty
    def main_keyboard(self) -> HyprlandKeyboard:
        """
        The main keyboard.
        """
        return self._main_keyboard

    @IgnisProperty
    def windows(self) -> list[HyprlandWindow]:
        """
        A list of windows.
        """
        return list(self._windows.values())

    @IgnisProperty
    def active_window(self) -> HyprlandWindow:
        """
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
        value_list = event_value.split(",")

        match event_type:
            case "destroyworkspacev2":
                self.__destroy_workspace(int(value_list[0]))
            case "createworkspacev2":
                self.__create_workspace(int(value_list[0]))
            case "workspace":
                self.__sync_active_workspace()
            case "focusedmon":
                self.__sync_active_workspace()
            case "activelayout":
                self.__sync_active_layout(value_list[1])
            case "activewindow":
                self.__sync_active_window()
            case "renameworkspace":
                self.__rename_workspace(int(value_list[0]), value_list[1])
            case "openwindow":
                self.__open_window(value_list[0])
            case "closewindow":
                self.__close_window(value_list[0])
            case "movewindowv2":
                self.__move_window(value_list[0], int(value_list[1]), value_list[0])
            case "changefloatingmode":
                self.__change_window_floating_mode(value_list[0], int(value_list[1]))
            case "windowtitlev2":
                # window title can contain comma (,)
                value_list = event_value.split(",", 1)
                self.__change_window_title(*value_list)
            case "pin":
                self.__change_window_pin_state(value_list[0], int(value_list[1]))

    def __initial_sync_workspaces(self) -> None:
        workspaces = json.loads(self.send_command("j/workspaces"))

        for workspace_data in workspaces:
            workspace = HyprlandWorkspace(self)
            workspace.sync(workspace_data)
            self._workspaces[workspace_data["id"]] = workspace

        self.__sort_workspaces()
        self.notify("workspaces")

    def __create_workspace(self, id_: int) -> None:
        for i in json.loads(self.send_command("j/workspaces")):
            if id_ == i["id"]:
                workspace_data = i
                break
        else:
            workspace_data = None

        if workspace_data:
            workspace = HyprlandWorkspace(self)
            workspace.sync(workspace_data)
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

    def __rename_workspace(self, workspace_id: int, new_name: str) -> None:
        workspace = self._workspaces.get(workspace_id, None)
        if workspace:
            workspace.sync({"name": new_name})

    def __sort_workspaces(self) -> None:
        self._workspaces = dict(sorted(self._workspaces.items()))

    def __sync_active_workspace(self) -> None:
        workspace_data = json.loads(self.send_command("j/activeworkspace"))
        self._active_workspace.sync(workspace_data)
        self.notify("active-workspace")

    def __sync_main_keyboard(self) -> None:
        data_list = json.loads(self.send_command("j/devices"))["keyboards"]

        for kb_data in data_list:
            if kb_data["main"] is True:
                self._main_keyboard.sync(kb_data)

        self.notify("main-keyboard")

    def __sync_active_layout(self, layout: str) -> None:
        self._main_keyboard.sync({"active_keymap": layout})

    def __sync_active_window(self) -> None:
        active_window_data = json.loads(self.send_command("j/activewindow"))
        self.active_window.sync(active_window_data)
        self.notify("active-window")

    def __initial_sync_windows(self) -> None:
        data = json.loads(self.send_command("j/clients"))

        for window_data in data:
            address = window_data["address"].replace("0x", "")

            window = HyprlandWindow()
            window.sync(window_data)
            self._windows[address] = window

        self.notify("windows")

    def __get_window_data(self, address: str) -> dict:
        for window in json.loads(self.send_command("j/clients")):
            if window["address"].replace("0x", "") == address:
                return window

        return {}

    def __sync_window_data(self, address: str, data: dict[str, Any]) -> None:
        window = self._windows.get(address, None)
        if window:
            window.sync(data)

    def __open_window(self, address: str) -> None:
        window_data = self.__get_window_data(address)
        window = HyprlandWindow()
        window.sync(window_data)
        self._windows[address] = window
        self.emit("window-added", window)
        self.notify("windows")

    def __close_window(self, address: str) -> None:
        window = self._windows.pop(address, None)
        if window:
            window.emit("closed")
            self.notify("windows")

    def __move_window(
        self, address: str, workspace_id: int, workspace_name: str
    ) -> None:
        self.__sync_window_data(
            address=address,
            data={"workspace": {"id": workspace_id, "name": workspace_name}},
        )

    def __change_window_floating_mode(self, address: str, floating: int) -> None:
        self.__sync_window_data(address=address, data={"floating": bool(floating)})

    def __change_window_title(self, address: str, title: str) -> None:
        self.__sync_window_data(address=address, data={"title": title})

    def __change_window_pin_state(self, address: str, pin_state: int) -> None:
        self.__sync_window_data(
            address=address, data={"title": {"pinned": bool(pin_state)}}
        )

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

    def get_window_by_address(self, address: str) -> HyprlandWindow | None:
        """
        Get a window by its address.

        Args:
            address: The address of the window.
        Returns:
            The window instance, or ``None`` if the window with the given address doesn't exist.
        """
        return self._windows.get(address, None)

    def get_windows_on_workspace(self, workspace_id: int) -> list[HyprlandWindow]:
        """
        Get a list of windows on a workspace by its ID.

        Args:
            workspace_id: The ID of the workspace.

        Returns:
            A list of windows on the workspace.
        """
        return [
            window
            for window in self._windows.values()
            if window.workspace_id == workspace_id
        ]
