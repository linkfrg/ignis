from ignis.dbus import DBusService
from gi.repository import GObject  # type: ignore
from ignis.utils import Utils
from ignis.gobject import IgnisGObject
from .action import NotificationAction


class Notification(IgnisGObject):
    """
    A notification object. Contain data about the notification and allows performing actions.

    Signals:
        - **"closed"** (): Emitted when notification has been closed.
        - **"dismissed"** (): Emitted when notification has been dismissed.

    Properties:
        - **id** (``int``, read-only): ID of the notification.
        - **app_name** (``int``, read-only): Name of the application that sent the notification.
        - **icon** (``str``, read-only): Icon name, path to image or ``None``.
        - **summary** (``int``, read-only): Summary text of the notification, usually the title.
        - **body** (``int``, read-only): Body text of the notification, usually containing additional information.
        - **actions** (list[:class:`~ignis.services.notifications.NotificationAction`], read-only): A list of actions associated with the notification.
        - **timeout** (``int``, read-only): Timeout for the notification. Usually equal to ``popup_timeout`` property of the :class:`~ignis.services.NotificationService` unless the notification specifies otherwise
        - **time** (``float``, read-only): Time in POSIX format when the notification was sent.
        - **popup** (``bool``, read-only):Whether the notification is a popup.

    """

    __gsignals__ = {
        "closed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "dismissed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(
        self,
        dbus: DBusService,
        id: int,
        app_name: str,
        icon: str,
        summary: str,
        body: str,
        actions: list[str],
        urgency: int,
        timeout: int,
        time: float,
        popup: bool,
    ):
        super().__init__()

        self.__dbus = dbus
        self._id = id
        self._app_name = app_name
        self._icon = icon
        self._summary = summary
        self._body = body
        self._timeout = timeout
        self._time = time
        self._urgency = urgency
        self._popup = popup
        self._actions = [
            NotificationAction(
                id=str(actions[i]),
                label=str(actions[i + 1]),
                dbus=self.__dbus,
                notification=self,
            )
            for i in range(0, len(actions), 2)
        ]

        Utils.Timeout(timeout, self.dismiss)

    @GObject.Property
    def id(self) -> int:
        return self._id

    @GObject.Property
    def app_name(self) -> str:
        return self._app_name

    @GObject.Property
    def icon(self) -> str:
        return self._icon

    @GObject.Property
    def summary(self) -> str:
        return self._summary

    @GObject.Property
    def body(self) -> str:
        return self._body

    @GObject.Property
    def actions(self) -> list["NotificationAction"]:
        return self._actions

    @GObject.Property
    def timeout(self) -> int:
        return self._timeout

    @GObject.Property
    def time(self) -> float:
        return self._time

    @GObject.Property
    def urgency(self) -> int:
        return self._urgency

    @GObject.Property
    def popup(self) -> bool:
        return self._popup

    @GObject.Property
    def json(self) -> dict:
        return {
            "id": self._id,
            "app_name": self._app_name,
            "icon": self._icon,
            "summary": self._summary,
            "body": self._body,
            "actions": [j for i in self._actions for j in (i.id, i.label)],
            "timeout": self._timeout,
            "time": self._time,
            "urgency": self._urgency,
        }

    def close(self) -> None:
        self.emit("closed")

    def dismiss(self) -> None:
        if self._popup:
            self._popup = False
            self.emit("dismissed")
            self.notify("popup")
