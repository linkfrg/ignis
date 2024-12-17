from gi.repository import Gio, GLib, GObject  # type: ignore
from ignis.dbus import DBusProxy
from ignis.utils import Utils
from ignis.logging import logger
from ignis.gobject import IgnisGObject
from typing import Literal


class SystemdUnit(IgnisGObject):
    """
    An object tracking a single systemd unit.

    """

    def __init__(self, object_path: str, bus_type: Literal["session", "system"]):
        super().__init__()

        self._object_path = object_path
        self._bus_type = bus_type

        if self._bus_type == "system":
            self._flags = Gio.DBusCallFlags.ALLOW_INTERACTIVE_AUTHORIZATION
        else:
            self._flags = Gio.DBusCallFlags.NONE

        self._proxy = DBusProxy(
            name="org.freedesktop.systemd1",
            object_path=self._object_path,
            interface_name="org.freedesktop.systemd1.Unit",
            info=Utils.load_interface_xml("org.freedesktop.systemd1.Unit"),
            bus_type=self._bus_type,
        )

        self._proxy.proxy.connect("g-properties-changed", self.__sync)

    def __handle_result(self, proxy, result, user_data) -> None:
        if isinstance(result, GLib.Error):
            logger.warning(
                f"[Systemd Service] Start/stop/restart request failed: {result.message}"
            )

    def start(self) -> None:
        """
        Start this unit.
        """
        self._proxy.Start(
            "(s)",
            "replace",
            flags=self._flags,
            result_handler=self.__handle_result,
        )

    def stop(self) -> None:
        """
        Stop this unit.
        """
        self._proxy.Stop(
            "(s)",
            "replace",
            flags=self._flags,
            result_handler=self.__handle_result,
        )

    def restart(self) -> None:
        """
        Restart this unit.
        """
        self._proxy.Restart(
            "(s)",
            "replace",
            flags=self._flags,
            result_handler=self.__handle_result,
        )

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
        state = self._proxy.ActiveState
        if state == "active":
            return True
        else:
            return False

    def __sync(self, proxy, properties: GLib.Variant, invalidated_properties) -> None:
        prop_dict = properties.unpack()

        if "ActiveState" in prop_dict.keys():
            self.notify("is-active")
