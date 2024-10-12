from ignis.base_service import BaseService
from gi.repository import GObject  # type: ignore
from ._imports import UPowerGlib
from .device import UPowerDevice


class UPowerService(BaseService):
    """
    An UPower service.
    Requires ``UPower``.

    Signals:
        - **device-added** (:class:`~ignis.services.upower.UPowerDevice`): Emitted when a power device has been added.
        - **battery-added** (:class:`~ignis.services.upower.UPowerDevice`): Emitted when a battery has been added.

    Properties:
        - **devices** (list[:class:`~ignis.services.upower.UPowerDevice`]): List of all power devices.
        - **batteries** (list[:class:`~ignis.services.upower.UPowerDevice`]): List of batteries.
        - **display_device** (:class:`~ignis.services.upower.UPowerDevice`): The currently active device intended for display.
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

        self._client = UPowerGlib.Client.new()
        self._devices: dict[str, UPowerDevice] = {}
        self._batteries: dict[str, UPowerDevice] = {}
        self._display_device = UPowerDevice(device=self._client.get_display_device())

        self._client.connect("device-added", self.__add_device)
        self._client.connect("device-removed", self.__remove_device)

        for device in self._client.get_devices():
            self.__add_device(None, device)

    @GObject.Property
    def devices(self) -> list[UPowerDevice]:
        return list(self._devices.values())

    @GObject.Property
    def batteries(self) -> list[UPowerDevice]:
        return list(self._batteries.values())

    @GObject.Property
    def display_device(self) -> UPowerDevice:
        return self._display_device

    def __add_device(self, x, gdevice: UPowerGlib.Device) -> None:
        device = UPowerDevice(device=gdevice)
        self._devices[gdevice.get_object_path()] = device
        self.emit("device-added", device)

        if gdevice.props.kind == UPowerGlib.DeviceKind.BATTERY:
            self._batteries[gdevice.get_object_path()] = device
            self.emit("battery-added", device)

    def __remove_device(self, x, object_path: str) -> None:
        if object_path not in self._devices:
            return

        if object_path in self._batteries:
            self._batteries.pop(object_path)

        device = self._devices.pop(object_path)
        device.emit("removed")
