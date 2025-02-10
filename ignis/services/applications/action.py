import os
import subprocess
from gi.repository import GObject, Gio, GLib  # type: ignore
from ignis.gobject import IgnisGObject


class ApplicationAction(IgnisGObject):
    """
    Application action.
    """

    def __init__(self, app: Gio.DesktopAppInfo, action: str):
        super().__init__()

        self._app = app
        self._action = action
        self._name: str = app.get_action_name(action)

    @GObject.Property
    def action(self) -> str:
        """
        - read-only

        The ID of the action.
        """
        return self._action

    @GObject.Property
    def name(self) -> str:
        """
        - read-only

        The human-readable name of the action.
        """
        return self._name

    def launch(self) -> None:
        """
        Launch this action.
        """
        self._app.launch_action(self.action, None)

    def launch_uwsm(self) -> None:
        """
            Launch the action using UWSM (Universal Wayland Session Manager).
        """
        custom_env = os.environ.copy()

        # Disable Python virtual environment
        custom_env.pop("VIRTUAL_ENV", None)
        custom_env.pop("PYTHONHOME", None)
        custom_env.pop("PYTHONPATH", None)
        custom_env["PATH"] = os.defpath

        cmd: str = f"uwsm app -- {self.desktop_file}:{self.action}"

        subprocess.Popen(
            cmd,
            shell=True,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=GLib.get_home_dir(),
            env=custom_env,
        )
