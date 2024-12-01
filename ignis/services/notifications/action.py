from ignis.dbus import DBusService
from gi.repository import GLib, GObject  # type: ignore
from ignis.gobject import IgnisGObject


class NotificationAction(IgnisGObject):
    """
    A simple object that contains data about a notification action.
    """

    def __init__(self, dbus: DBusService, notification, id: str, label: str):
        super().__init__()
        self.__dbus = dbus
        self.__notification = notification
        self._id = id
        self._label = label

    @GObject.Property
    def id(self) -> str:
        """
        - read-only

        The ID of the action.
        """
        return self._id

    @GObject.Property
    def label(self) -> str:
        """
        - read-only

        The label of the notification. This one should be displayed to user.
        """
        return self._label

    def invoke(self) -> None:
        """
        Invoke this action.
        """
        self.__dbus.emit_signal(
            "ActionInvoked", GLib.Variant("(us)", (self.__notification.id, self.id))
        )
