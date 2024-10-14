from __future__ import annotations
from gi.repository import GObject, Gio  # type: ignore
from ignis.base_service import BaseService
from .application import Application
from ignis.services.options import OptionsService


class ApplicationsService(BaseService):
    """
    Provides a list of applications installed on the system.
    It also allows "pinning" of apps and retrieving a list of pinned applications.

    Properties:
        - **apps** (list[:class:`~ignis.services.applications.Application`], read-only): A list of all installed applications.
        - **pinned** (list[:class:`~ignis.services.applications.Application`], read-only): A list of all pinned applications.

    **Example usage**:

    .. code-block:: python

        from ignis.services.applications import ApplicationsService

        applications = ApplicationsService.get_default()
        for i in applications.apps:
            print(i.name)

    """

    def __init__(self):
        super().__init__()
        self._apps: dict[str, Application] = {}
        self._pinned: dict[str, Application] = {}

        self._monitor = Gio.AppInfoMonitor.get()
        self._monitor.connect("changed", lambda x: self.__sync())

        options = OptionsService.get_default()
        opt_group = options.create_group(name="applications", exists_ok=True)
        self._pinned_apps_opt = opt_group.create_option(
            name="pinned_apps", default=[], exists_ok=True
        )

        self.__sync()

    @GObject.Property
    def apps(self) -> list[Application]:
        return sorted(self._apps.values(), key=lambda x: x.name)

    @GObject.Property
    def pinned(self) -> list[Application]:
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
        for pinned in self._pinned_apps_opt.value:
            try:
                app = Gio.DesktopAppInfo.new(desktop_id=pinned)
            except TypeError:
                continue
            if not app:
                return

            entry = Application(app=app, is_pinned=True)
            self.__connect_entry(entry)
            self._pinned[entry.id] = entry

    def search(self, query: str) -> list[Application]:
        """
        Filter applications by query.

        Args:
            query (str): the string to be searched for

        Returns:
            list[Application]: A list of applications filtered by provided query.
        """
        return [
            entry
            for result in Gio.DesktopAppInfo.search(query)
            for entry in self.apps
            if entry.id in result
        ]

    def __sync_pinned(self) -> None:
        pinned_ids = [p.id for p in self.pinned]
        self._pinned_apps_opt.value = pinned_ids
        self.notify("pinned")

    def __pin_entry(self, entry: Application) -> None:
        self._pinned[entry.id] = entry
        self.__sync_pinned()

    def __unpin_entry(self, entry: Application) -> None:
        self._pinned.pop(entry.id)
        self.__sync_pinned()
