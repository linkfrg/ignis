from ignis.dbus import DBusProxy
from ignis.utils import Utils
from ignis.base_service import BaseService


class SystemdService(BaseService):
    """
    A service for controlling systemd units through DBus.

    Example usage:

    .. code-block:: python

        from ignis.services.systemd import SystemdService

        systemd = SystemdService.get_default()

        systemd.start_unit("rot8.service")
    """

    def __init__(self) -> None:
        super().__init__()

        self.__dbus = DBusProxy(
            name="org.freedesktop.systemd1",
            object_path="/org/freedesktop/systemd1",
            interface_name="org.freedesktop.systemd1.Manager",
            info=Utils.load_interface_xml("org.freedesktop.systemd1.Manager"),
            bus_type="session",
        )

    def start_unit(self, unit: str) -> None:
        self.__dbus.proxy.StartUnit("(ss)", unit, "replace")

    def stop_unit(self, unit: str) -> None:
        self.__dbus.proxy.StopUnit("(ss)", unit, "replace")

    def restart_unit(self, unit: str) -> None:
        self.__dbus.proxy.RestartUnit("(ss)", unit, "replace")
