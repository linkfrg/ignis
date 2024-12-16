from __future__ import annotations
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

    _session_instance: SystemdService | None = None
    _system_instance: SystemdService | None = None

    def __init__(self, bus_type: Literal["session", "system"] = "session") -> None:
        super().__init__()

        self._proxy = DBusProxy(
            name="org.freedesktop.systemd1",
            object_path="/org/freedesktop/systemd1",
            interface_name="org.freedesktop.systemd1.Manager",
            info=Utils.load_interface_xml("org.freedesktop.systemd1.Manager"),
            bus_type=bus_type,
        )

    @classmethod
    def get_default(  # type: ignore
        cls: SystemdService, bus_type: Literal["session", "system"] = "session"
    ) -> SystemdService:
        """
        Returns the default Service object for this process, creating it if necessary.

        Args:
            bus_type: The bus type.

        Bus types:
            - session: current user session
            - system: entire system, requires interactive authorization when calling methods
        """
        if bus_type not in ("session", "system"):
            raise TypeError(f"Invalid bus type: {bus_type}")

        instance_attr = f"_{bus_type}_instance"

        if getattr(cls, instance_attr) is None:
            setattr(cls, instance_attr, cls(bus_type))  # type: ignore
        return getattr(cls, instance_attr)

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
        object_path = self._proxy.proxy.LoadUnit("(s)", unit)
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
        for item in self._proxy.proxy.ListUnitFiles():
            unit_name = os.path.basename(item[0])
            if "@" not in unit_name:
                units.append(self.get_unit(unit_name, bus_type))

        return units
