import os
import re
import subprocess
from gi.repository import GObject, Gio, GLib  # type: ignore
from ignis.gobject import IgnisGObject, IgnisProperty
from .action import ApplicationAction


class Application(IgnisGObject):
    """
    An application object.
    """

    def __init__(self, app: Gio.DesktopAppInfo, is_pinned: bool):
        super().__init__()

        self._app = app
        self._is_pinned = is_pinned
        self._actions: list[ApplicationAction] = []

        for action in app.list_actions():
            self._actions.append(ApplicationAction(app=app, action=action))

    @GObject.Signal
    def pinned(self):
        """
        - Signal

        Emitted when the application has been pinned.
        """

    @GObject.Signal
    def unpinned(self):
        """
        - Signal

        Emitted when the application has been unpinned.
        """

    @IgnisProperty
    def app(self) -> Gio.DesktopAppInfo:
        """
        - read-only

        An instance of :class:`Gio.DesktopAppInfo`.
        """
        return self._app

    @IgnisProperty
    def id(self) -> str | None:
        """
        - read-only

        The ID of the application.
        """
        return self._app.get_id()

    @IgnisProperty
    def name(self) -> str:
        """
        - read-only

        The name of the application.
        """
        return self._app.get_display_name()

    @IgnisProperty
    def description(self) -> str | None:
        """
        - read-only

        The description of the application.
        """
        return self._app.get_description()

    @IgnisProperty
    def icon(self) -> str:
        """
        - read-only

        The icon of the application. If the app has no icon, "image-missing" will be returned.
        """
        icon = self._app.get_string("Icon")
        if not icon:
            return "image-missing"
        else:
            return icon

    @IgnisProperty
    def keywords(self) -> list[str]:
        """
        - read-only

        Keywords of the application. Ususally, these are words that describe the application.
        """
        return self._app.get_keywords()

    @IgnisProperty
    def desktop_file(self) -> str | None:
        """
        - read-only

        The full path to the ``.desktop`` file of the application.
        """
        return self._app.get_filename()

    @IgnisProperty
    def executable(self) -> str:
        """
        - read-only

        The executable of the application.
        """
        return self._app.get_executable()

    @IgnisProperty
    def exec_string(self) -> str | None:
        """
        - read-only

        The string that contains the executable with command line arguments, used to launch the application.
        """
        return self._app.get_string("Exec")

    @IgnisProperty
    def actions(self) -> list[ApplicationAction]:
        """
        - read-only

        A list of actions.
        """
        return self._actions

    @IgnisProperty
    def is_pinned(self) -> bool:
        """
        - read-write

        Whether the application is pinned.
        """
        return self._is_pinned

    @is_pinned.setter
    def is_pinned(self, value: bool) -> None:
        if value == self._is_pinned:
            return

        self._is_pinned = value
        if value:
            self.emit("pinned")
        else:
            self.emit("unpinned")

    @IgnisProperty
    def is_terminal(self) -> bool:
        """
        - read-only

        Whether the application has to be launched in a terminal.
        """
        return {"true": True, "false": False, None: False}.get(
            self._app.get_string("Terminal"), False
        )

    def pin(self) -> None:
        """
        Pin the application.
        """
        self.is_pinned = True

    def unpin(self) -> None:
        """
        Unpin the application.
        """
        self.is_pinned = False

    def launch(
        self, command_format: str | None = None, terminal_format: str | None = None
    ) -> None:
        """
        Launch the application.

        Args:
            command_format: A format string for the command to launch. ``%command%`` will be replaced with the actual command. Shell syntax is supported.
            terminal_format: A format string for the command to launch if the application has to be run in a terminal. ``%command%`` will be replaced with the actual command. Shell syntax is supported.

        To launch terminal applications, pass the ``terminal_format`` argument:

        .. code-block:: python

            # kitty for example, format may differ for other terminals
            APPLICATION.launch(terminal_format="kitty %command%")
        """
        exec_string = re.sub(r"%\S*", "", self.exec_string)
        custom_env = os.environ.copy()

        # Disable Python virtual environment
        custom_env.pop("VIRTUAL_ENV", None)
        custom_env.pop("PYTHONHOME", None)
        custom_env.pop("PYTHONPATH", None)
        custom_env["PATH"] = os.defpath

        cmd: str

        if self.is_terminal is True and terminal_format is not None:
            cmd = terminal_format.replace("%command%", exec_string)
        elif command_format is not None:
            cmd = command_format.replace("%command%", exec_string)
        else:
            cmd = exec_string

        subprocess.Popen(
            cmd,
            shell=True,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=GLib.get_home_dir(),
            env=custom_env,
        )

    def launch_uwsm(self) -> None:
        """
        Launch the application using UWSM (Universal Wayland Session Manager).
        """
        custom_env = os.environ.copy()

        # Disable Python virtual environment
        custom_env.pop("VIRTUAL_ENV", None)
        custom_env.pop("PYTHONHOME", None)
        custom_env.pop("PYTHONPATH", None)
        custom_env["PATH"] = os.defpath

        cmd: str = f"uwsm app -- {self.desktop_file}"

        subprocess.Popen(
            cmd,
            shell=True,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=GLib.get_home_dir(),
            env=custom_env,
        )
