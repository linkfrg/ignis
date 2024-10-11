from ignis.base_service import BaseService
from gi.repository import GObject  # type: ignore
from ._imports import UPowerGlib
from .battery import Battery


class BatteryService(BaseService):
    """
    A battery service.
    Requires ``UPower``.

    Signals:
        - **device-added** (:class:`~ignis.services.battery.Battery`): Emitted when a battery has been added.

    Properties:
        - **devices** (list[:class:`~ignis.services.battery.Battery`]): List of all batteries.
        - **display_device** (:class:`~ignis.services.battery.Battery`): The currently active battery intended for display.
    """

    __gsignals__ = {
        "device-added": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (Battery,)),
    }

    def __init__(self) -> None:
        super().__init__()

        self._client = UPowerGlib.Client.new()
        self._devices: dict[str, Battery] = {}
        self._display_device = Battery(device=self._client.get_display_device())

        self._client.connect("device-added", self.__add_device)
        self._client.connect("device-removed", self.__remove_device)

        for device in self._client.get_devices():
            self.__add_device(None, device)

    @GObject.Property
    def devices(self) -> list[Battery]:
        return list(self._devices.values())

    @GObject.Property
    def display_device(self) -> Battery:
        return self._display_device

    def __add_device(self, x, device: UPowerGlib.Device) -> None:
        if (
            device.props.kind != UPowerGlib.DeviceKind.BATTERY
        ):  # don't add non-battery devices
            return

        battery = Battery(device=device)

        self._devices[device.get_object_path()] = battery

        self.emit("device-added", battery)

    def __remove_device(self, x, object_path: str) -> None:
        if object_path not in self._devices:
            return
        battery = self._devices.pop(object_path)
        battery.emit("removed")
