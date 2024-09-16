import re
import subprocess
from gi.repository import GObject, Gio  # type: ignore
from ignis.gobject import IgnisGObject
from .action import ApplicationAction


class Application(IgnisGObject):
    """
    An application object.

    Signals:
        - **"pinned"**: Emitted when the application has been pinned.
        - **"unpinned"**: Emitted when the application has been unpinned.

    Properties:
        - **app** (`Gio.DesktopAppInfo <https://lazka.github.io/pgi-docs/index.html#Gio-2.0/classes/DesktopAppInfo.html>`_, read-only): An instance of ``Gio.DesktopAppInfo``. You typically shouldn't use this property.
        - **id** (``str | None``, read-only): The ID of the application.
        - **name** (``str``, read-only): The name of the application.
        - **description** (``str | None``, read-only): The description of the application.
        - **icon** (``str``, read-only): The icon of the application. If the app has no icon, "image-missing" will be returned.
        - **keywords** (``list[str]``, read-only): Keywords of the application. Ususally, these are words that describe the application.
        - **desktop_file** (``str | None``, read-only): The full path to the ``.desktop`` file of the application.
        - **executable** (``str | None``, read-only): The executable of the application.
        - **exec_string** (``str``, read-only): The string that contains the executable with command line arguments, used to launch the application.
        - **actions** (list[:class:`~ignis.services.applications.Application`], read-only): A list of actions.
        - **is_pinned** (``bool``, read-write): Whether the application is pinned.
    """

    __gsignals__ = {
        "pinned": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "unpinned": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, app: Gio.DesktopAppInfo, is_pinned: bool):
        super().__init__()

        self._app = app
        self._is_pinned = is_pinned
        self._actions: list[ApplicationAction] = []

        for action in app.list_actions():
            self._actions.append(ApplicationAction(app=app, action=action))

    @GObject.Property
    def app(self) -> Gio.DesktopAppInfo:
        return self._app

    @GObject.Property
    def id(self) -> str | None:
        return self._app.get_id()

    @GObject.Property
    def name(self) -> str:
        return self._app.get_display_name()

    @GObject.Property
    def description(self) -> str | None:
        return self._app.get_description()

    @GObject.Property
    def icon(self) -> str:
        icon = self._app.get_string("Icon")
        if not icon:
            return "image-missing"
        else:
            return icon

    @GObject.Property
    def keywords(self) -> list[str]:
        return self._app.get_keywords()

    @GObject.Property
    def desktop_file(self) -> str | None:
        return self._app.get_filename()

    @GObject.Property
    def executable(self) -> str:
        return self._app.get_executable()

    @GObject.Property
    def exec_string(self) -> str | None:
        return self._app.get_string("Exec")

    @GObject.Property
    def actions(self) -> list[ApplicationAction]:
        return self._actions

    @GObject.Property
    def is_pinned(self) -> bool:
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
        subprocess.Popen(
            exec_string,
            shell=True,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
