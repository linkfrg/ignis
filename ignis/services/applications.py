import re
import subprocess
from gi.repository import GObject, Gio  # type: ignore
from ignis.gobject import IgnisGObject
from typing import List, Dict
from ignis.services import Service

PINNED_APPS_OPTION = "pinned_apps"


class ApplicationAction(IgnisGObject):
    """
    Application action.

    Properties:
        - **action** (``str``, read-only): ID of the action.
        - **name** (``str``, read-only): Human-readable name of the action.
    """

    def __init__(self, app: Gio.DesktopAppInfo, action: str):
        super().__init__()

        self._app = app
        self._action = action
        self._name: str = app.get_action_name(action)

    @GObject.Property
    def action(self) -> str:
        return self._action

    @GObject.Property
    def name(self) -> str:
        return self._name

    def launch(self) -> None:
        """
        Launch action.
        """
        self._app.launch_action(self.action, None)


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
        - **keywords** (``List[str]``, read-only): Keywords of the application. Ususally, these are words that describe the application.
        - **desktop_file** (``str | None``, read-only): The full path to the ``.desktop`` file of the application.
        - **executable** (``str | None``, read-only): The executable of the application.
        - **exec_string** (``str``, read-only): The string that contains the executable with command line arguments, used to launch the application.
        - **actions** (List[:class:`~ignis.services.applications.Application`], read-only): A list of actions.
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
        self._actions: List[ApplicationAction] = []

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
    def keywords(self) -> List[str]:
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
    def actions(self) -> List[ApplicationAction]:
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


class ApplicationsService(IgnisGObject):
    """
    Provides a list of applications installed on the system.
    It also allows "pinning" of apps and retrieving a list of pinned applications.

    Properties:
        - **apps** (List[:class:`~ignis.services.applications.Application`], read-only): A list of all installed applications.
        - **pinned** (List[:class:`~ignis.services.applications.Application`], read-only): A list of all pinned applications.

    **Example usage**:

    .. code-block:: python

        from ignis.service import Service

        applications = Service.get("applications")
        for i in applications.apps:
            print(i.name)

    """

    def __init__(self):
        super().__init__()
        self._apps: Dict[str, Application] = {}
        self._pinned: Dict[str, Application] = {}

        self._monitor = Gio.AppInfoMonitor.get()
        self._monitor.connect("changed", lambda x: self.__sync())

        self._options = Service.get("options")
        self._options.create_option(name=PINNED_APPS_OPTION, default=[], exists_ok=True)

        self.__sync()

    @GObject.Property
    def apps(self) -> List[Application]:
        return sorted(self._apps.values(), key=lambda x: x.name)

    @GObject.Property
    def pinned(self) -> List[Application]:
        return list(self._pinned.values())

    def __connect_entry(self, entry: Application) -> None:
        entry.connect("pinned", lambda x: self.__pin_entry(x))
        entry.connect("unpinned", lambda x: self.__unpin_entry(x))

    def __sync(self) -> None:
        self._apps = {}
        self._pinned = {}
        self.__read_pinned_apps()
        for app in Gio.AppInfo.get_all():
            if isinstance(app, Gio.DesktopAppInfo):
                self.__add_app(app)

        self.notify("apps")
        self.notify("pinned")

    def __add_app(self, app: Gio.DesktopAppInfo) -> None:
        if app.get_nodisplay():
            return

        if app.get_id() in self._pinned:
            entry = Application(app=app, is_pinned=True)
        else:
            entry = Application(app=app, is_pinned=False)

        self.__connect_entry(entry)
        self._apps[entry.id] = entry

    def __read_pinned_apps(self) -> None:
        for pinned in self._options.get_option(PINNED_APPS_OPTION):
            try:
                app = Gio.DesktopAppInfo.new(desktop_id=pinned)
            except TypeError:
                continue
            if not app:
                return

            entry = Application(app=app, is_pinned=True)
            self.__connect_entry(entry)
            self._pinned[entry.id] = entry

    def search(self, query: str) -> List[Application]:
        """
        Filter applications by query.

        Args:
            query (str): the string to be searched for

        Returns:
            List[Application]: List of applications filtered by provided query.
        """
        return [
            entry
            for result in Gio.DesktopAppInfo.search(query)
            for entry in self.apps
            if entry.id in result
        ]

    def __sync_pinned(self) -> None:
        pinned_ids = [p.id for p in self.pinned]
        self._options.set_option(PINNED_APPS_OPTION, pinned_ids)
        self.notify("pinned")

    def __pin_entry(self, entry: Application) -> None:
        self._pinned[entry.id] = entry
        self.__sync_pinned()

    def __unpin_entry(self, entry: Application) -> None:
        self._pinned.pop(entry.id)
        self.__sync_pinned()
