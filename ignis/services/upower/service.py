from ignis.base_service import BaseService
from ignis.dbus import DBusProxy
from ignis.utils import Utils
from ignis.exceptions import UPowerNotRunningError
from ignis.gobject import IgnisProperty, IgnisSignal
from .device import UPowerDevice


class UPowerService(BaseService):
    """
    An UPower service.
    Requires ``UPower``.

    Raises:
        UPowerNotRunningError: If UPower D-Bus service is not running.
    """

    def __init__(self) -> None:
        super().__init__()

        self._proxy = DBusProxy.new(
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

    @IgnisSignal
    def device_added(self, device: UPowerDevice):
        """
        Emitted when a power device has been added.

        Args:
            device: The instance of the UPower device.
        """

    @IgnisSignal
    def battery_added(self, battery: UPowerDevice):
        """
        Emitted when a battery has been added.

        Args:
            battery: The instance of the battery.
        """

    @IgnisProperty
    def devices(self) -> list[UPowerDevice]:
        """
        A list of all power devices.
        """
        return list(self._devices.values())

    @IgnisProperty
    def batteries(self) -> list[UPowerDevice]:
        """
        A list of batteries.
        """
        return list(self._batteries.values())

    @IgnisProperty
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
