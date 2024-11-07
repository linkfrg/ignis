from ignis.dbus import DBusService
from gi.repository import GObject  # type: ignore
from ignis.utils import Utils
from ignis.gobject import IgnisGObject
from .action import NotificationAction


class Notification(IgnisGObject):
    """
    A notification object.
    Contains data about the notification and allows performing actions.
    """

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

    @GObject.Signal
    def closed(self):
        """
        - Signal

        Emitted when notification has been closed.
        """

    @GObject.Signal
    def dismissed(self):
        """
        - Signal

        Emitted when notification has been dismissed.
        """

    @GObject.Property
    def id(self) -> int:
        """
        - read-only

        The ID of the notification.
        """
        return self._id

    @GObject.Property
    def app_name(self) -> str:
        """
        - read-only

        The name of the application that sent the notification.
        """
        return self._app_name

    @GObject.Property
    def icon(self) -> str:
        """
        - read-only

        The icon name, path to image or ``None``.
        """
        return self._icon

    @GObject.Property
    def summary(self) -> str:
        """
        - read-only

        The summary text of the notification, usually the title.
        """
        return self._summary

    @GObject.Property
    def body(self) -> str:
        """
        - read-only

        The body text of the notification, usually containing additional information.
        """
        return self._body

    @GObject.Property
    def actions(self) -> list["NotificationAction"]:
        """
        - read-only

        A list of actions associated with the notification.
        """
        return self._actions

    @GObject.Property
    def timeout(self) -> int:
        """
        - read-only

        The timeout for the notification.
        Usually equal to the ``popup_timeout`` property of the :class:`~ignis.services.NotificationService` unless the notification specifies otherwise.
        """
        return self._timeout

    @GObject.Property
    def time(self) -> float:
        """
        - read-only

        Time in POSIX format when the notification was sent.
        """
        return self._time

    @GObject.Property
    def urgency(self) -> int:
        """
        - read-only

        The urgency of the notification.

        Levels:
            - -1: Not provided
            - 0: Low
            - 1: Normal
            - 2: Critical
        """
        return self._urgency

    @GObject.Property
    def popup(self) -> bool:
        """
        - read-only

        Whether the notification is a popup.
        """
        return self._popup

    @GObject.Property
    def json(self) -> dict:
        """
        - read-only

        The notification data in dictionary format.
        """
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
        """
        Close the notification.
        This will remove it from notifications history.
        """
        self.emit("closed")

    def dismiss(self) -> None:
        """
        Dismiss the notification.
        """
        if self._popup:
            self._popup = False
            self.emit("dismissed")
            self.notify("popup")
