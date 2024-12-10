from gi.repository import GObject  # type: ignore

from ignis.dbus import DBusProxy
from ignis.utils import Utils
from ignis.gobject import IgnisGObject


class SystemdUnit(IgnisGObject):
    """
    An object for tracking the state of a single systemd unit.

    Example usage:

    .. code-block:: python

        from ignis.services.systemd import SystemdUnit

        active = SystemdUnit("rot8.service").bind("is_active")
    """

    def __init__(self, unit: str):
        super().__init__()

        self.__dbus = DBusProxy(
            name="org.freedesktop.systemd1",
            object_path="/org/freedesktop/systemd1",
            interface_name="org.freedesktop.systemd1.Manager",
            info=Utils.load_interface_xml("org.freedesktop.DBus"),
            bus_type="session",
        )

        unit_path = self.__dbus.proxy.LoadUnit("(s)", unit)

        self.__service_proxy = DBusProxy(
            name="org.freedesktop.systemd1",
            object_path=unit_path,
            interface_name="org.freedesktop.DBus.Properties",
            info=Utils.load_interface_xml("org.freedesktop.DBus"),
            bus_type="session",
        )

        self._is_active = self.__is_unit_active()
        self.__subscribe_unit()

    @GObject.Property
    def is_active(self) -> bool:
        """
        - read-only

        Whether the unit is active (running).
        """
        return self._is_active

    def __is_unit_active(self) -> bool:
        state = self.__service_proxy.proxy.Get(
            "(ss)", "org.freedesktop.systemd1.Unit", "ActiveState"
        )
        if state == "active":
            self._is_active = True
        else:
            self._is_active = False

        self.notify("is_active")
        return self._is_active

    def __update_state(self, *args) -> None:
        body = args[5][1]
        try:
            if body["ActiveState"] == "active":
                self._is_active = True
            else:
                self._is_active = False

        except KeyError:
            pass

        self.notify("is_active")

    def __subscribe_unit(self) -> None:
        self.__service_proxy.signal_subscribe(
            signal_name="PropertiesChanged",
            callback=self.__update_state,
        )
