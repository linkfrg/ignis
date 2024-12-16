from gi.repository import Gio, GObject  # type: ignore

from ignis.dbus import DBusProxy
from ignis.utils import Utils
from ignis.logging import logger
from ignis.gobject import IgnisGObject

from typing import Literal


class SystemdUnit(IgnisGObject):
    """
    An object tracking a single systemd unit.

    """

    def __init__(
        self, unit: str, object_path: str, bus_type: Literal["session", "system"]
    ):
        super().__init__()

        self._unit = unit
        self._object_path = object_path
        self._bus_type = bus_type

        if self._bus_type == "system":
            self._flags = Gio.DBusCallFlags.ALLOW_INTERACTIVE_AUTHORIZATION
        else:
            self._flags = Gio.DBusCallFlags.NONE

        self.__manager_proxy = DBusProxy(
            name="org.freedesktop.systemd1",
            object_path="/org/freedesktop/systemd1",
            interface_name="org.freedesktop.systemd1.Manager",
            info=Utils.load_interface_xml("org.freedesktop.systemd1.Manager"),
            bus_type=self._bus_type,
        )

        self.__service_proxy = DBusProxy(
            name="org.freedesktop.systemd1",
            object_path=self._object_path,
            interface_name="org.freedesktop.DBus.Properties",
            info=Utils.load_interface_xml("org.freedesktop.DBus.Properties"),
            bus_type=self._bus_type,
        )

        self._is_active = self.__is_unit_active()
        self.__subscribe_unit()

    def start_unit(self) -> None:
        """
        Start this unit.
        """
        try:
            self.__manager_proxy.proxy.StartUnit("(ss)", self._unit, "replace", flags=self._flags)
        except Exception as e:
            logger.warning(f"[Systemd Service] Failed to start unit {self._unit}: {e}")

    def stop_unit(self) -> None:
        """
        Stop this unit.
        """
        try:
            self.__manager_proxy.proxy.StopUnit("(ss)", self._unit, "replace", flags=self._flags)
        except Exception as e:
            logger.warning(f"[Systemd Service] Failed to stop unit {self._unit}: {e}")

    def restart_unit(self) -> None:
        """
        Restart this unit.
        """
        try:
            self.__manager_proxy.proxy.RestartUnit("(ss)", self._unit, "replace", flags=self._flags)
        except Exception as e:
            logger.warning(f"[Systemd Service] Failed to restart unit {self._unit}: {e}")

    @GObject.Property
    def name(self) -> str:
        """
        - read-only

        The name of the unit.
        """
        return self._unit

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
