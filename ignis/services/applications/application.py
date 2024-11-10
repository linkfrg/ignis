import os
import re
import subprocess
from gi.repository import GObject, Gio, GLib  # type: ignore
from ignis.gobject import IgnisGObject
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

    @GObject.Property
    def app(self) -> Gio.DesktopAppInfo:
        """
        - read-only

        An instance of :class:`Gio.DesktopAppInfo`.
        """
        return self._app

    @GObject.Property
    def id(self) -> str | None:
        """
        - read-only

        The ID of the application.
        """
        return self._app.get_id()

    @GObject.Property
    def name(self) -> str:
        """
        - read-only

        The name of the application.
        """
        return self._app.get_display_name()

    @GObject.Property
    def description(self) -> str | None:
        """
        - read-only

        The description of the application.
        """
        return self._app.get_description()

    @GObject.Property
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

    @GObject.Property
    def keywords(self) -> list[str]:
        """
        - read-only

        Keywords of the application. Ususally, these are words that describe the application.
        """
        return self._app.get_keywords()

    @GObject.Property
    def desktop_file(self) -> str | None:
        """
        - read-only

        The full path to the ``.desktop`` file of the application.
        """
        return self._app.get_filename()

    @GObject.Property
    def executable(self) -> str:
        """
        - read-only

        The executable of the application.
        """
        return self._app.get_executable()

    @GObject.Property
    def exec_string(self) -> str | None:
        """
        - read-only

        The string that contains the executable with command line arguments, used to launch the application.
        """
        return self._app.get_string("Exec")

    @GObject.Property
    def actions(self) -> list[ApplicationAction]:
        """
        - read-only

        A list of actions.
        """
        return self._actions

    @GObject.Property
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

    def launch(self) -> None:
        """
        Launch the application.
        """
        exec_string = re.sub(r"%\S*", "", self.exec_string)
        custom_env = os.environ.copy()

        # Disable Python virtual environment
        custom_env.pop("VIRTUAL_ENV", None)
        custom_env.pop("PYTHONHOME", None)
        custom_env.pop("PYTHONPATH", None)
        custom_env["PATH"] = os.defpath

        subprocess.Popen(
            exec_string,
            shell=True,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=GLib.get_home_dir(),
            env=custom_env,
        )
