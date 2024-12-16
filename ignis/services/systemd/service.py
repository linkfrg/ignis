import os
from gi.repository import GObject  # type: ignore

from ignis.dbus import DBusProxy
from ignis.utils import Utils
from ignis.base_service import BaseService

from typing import Literal
from .unit import SystemdUnit


class SystemdService(BaseService):
    """
    A service for managing systemd units through DBus.

    Example usage:

    .. code-block:: python

        from ignis.services.systemd import SystemdService

        systemd = SystemdService.get_default()

        example_unit = systemd.get_unit("wluma.service")
        example_status = example_unit.bind("is_active")
        example_unit.restart()

    """

    def __init__(self) -> None:
        super().__init__()

    def __get_proxy(self, bus_type: Literal["session", "system"]) -> DBusProxy:
        """
        Returns a dbus proxy for the given bus type.
        """
        self.__manager_proxy = DBusProxy(
            name="org.freedesktop.systemd1",
            object_path="/org/freedesktop/systemd1",
            interface_name="org.freedesktop.systemd1.Manager",
            info=Utils.load_interface_xml("org.freedesktop.systemd1.Manager"),
            bus_type=bus_type,
        )
        return self.__manager_proxy

    def get_unit(
        self, unit: str, bus_type: Literal["session", "system"] = "session"
    ) -> SystemdUnit:
        """
        Get :class:`~ignis.services.systemd.SystemdUnit` by unit name.

        Args:
            unit: The name of the unit to get.
            bus_type: The systemd bus to query ("session" or "system"). Default is "session".

        Returns:
            :class:`~ignis.services.systemd.SystemdUnit`
        """
        object_path = self.__get_proxy(bus_type).proxy.LoadUnit("(s)", unit)
        return SystemdUnit(unit, object_path, bus_type)

    @GObject.Property
    def units(
        self, bus_type: Literal["session", "system"] = "session"
    ) -> list[SystemdUnit]:
        """
        - read-only

        A list of all systemd units, for a given bus (defaults to the "session" bus).
        """
        units = []
        for item in self.__get_proxy(bus_type).proxy.ListUnitFiles():
            unit_name = os.path.basename(item[0])
            if "@" not in unit_name:
                units.append(self.get_unit(unit_name, bus_type))

        return units
