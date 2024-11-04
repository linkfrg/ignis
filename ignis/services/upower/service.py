from ignis.base_service import BaseService
from gi.repository import GObject  # type: ignore
from ignis.dbus import DBusProxy
from ignis.utils import Utils
from ignis.exceptions import UPowerNotRunningError
from .device import UPowerDevice


class UPowerService(BaseService):
    """
    An UPower service.
    Requires ``UPower``.

    Signals:
        - **device-added** (:class:`~ignis.services.upower.UPowerDevice`): Emitted when a power device has been added.
        - **battery-added** (:class:`~ignis.services.upower.UPowerDevice`): Emitted when a battery has been added.

    Raises:
        UPowerNotRunningError: If UPower D-Bus service is not running.
    """

    __gsignals__ = {
        "device-added": (
            GObject.SignalFlags.RUN_FIRST,
            GObject.TYPE_NONE,
            (UPowerDevice,),
        ),
        "battery-added": (
            GObject.SignalFlags.RUN_FIRST,
            GObject.TYPE_NONE,
            (UPowerDevice,),
        ),
    }

    def __init__(self) -> None:
        super().__init__()

        self._proxy = DBusProxy(
            name="org.freedesktop.UPower",
            object_path="/org/freedesktop/UPower",
            interface_name="org.freedesktop.UPower",
            info=Utils.load_interface_xml("org.freedesktop.UPower"),
            bus_type="system",
        )

        if not self._proxy.has_owner:
            raise UPowerNotRunningError()

        self._devices: dict[str, UPowerDevice] = {}
        self._batteries: dict[str, UPowerDevice] = {}
        self._display_device = UPowerDevice(object_path=self._proxy.GetDisplayDevice())

        self._proxy.signal_subscribe(
            "DeviceAdded",
            lambda *args: self.__add_device(self.__get_device_object_path(args)),
        )
        self._proxy.signal_subscribe(
            "DeviceRemoved",
            lambda *args: self.__remove_device(self.__get_device_object_path(args)),
        )

        for device in self._proxy.EnumerateDevices():
            self.__add_device(device)

    def __get_device_object_path(self, args) -> str:
        return args[-1].unpack()[0]  # -1 element is the device object path (Variant)

    @GObject.Property
    def devices(self) -> list[UPowerDevice]:
        """
        A list of all power devices.
        """
        return list(self._devices.values())

    @GObject.Property
    def batteries(self) -> list[UPowerDevice]:
        """
        A list of batteries.
        """
        return list(self._batteries.values())

    @GObject.Property
    def display_device(self) -> UPowerDevice:
        """
        The currently active device intended for display.
        """
        return self._display_device

    def __add_device(self, object_path: str) -> None:
        device = UPowerDevice(object_path=object_path)
        self._devices[object_path] = device
        self.emit("device-added", device)

        if device.kind == "battery":
            self._batteries[object_path] = device
            self.emit("battery-added", device)

        self.notify("devices")

    def __remove_device(self, object_path: str) -> None:
        if object_path not in self._devices:
            return

        if object_path in self._batteries:
            self._batteries.pop(object_path)

        device = self._devices.pop(object_path)
        device.emit("removed")
        self.notify("devices")
