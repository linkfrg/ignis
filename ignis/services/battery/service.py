from ignis.base_service import BaseService
from gi.repository import GObject  # type: ignore
from ._imports import UPowerGlib
from .battery import Battery


class BatteryService(BaseService):
    """
    A battery service.

    Properties:
        - **devices** (list[:class:`~ignis.services.battery.Battery`]): List of all batteries.
        - **display_device** (:class:`~ignis.services.battery.Battery`): The currently active battery intended for display.
    """

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

        self._devices[device.get_object_path()] = Battery(device=device)

    def __remove_device(self, x, device: UPowerGlib.Device) -> None:
        if device.get_object_path() in self._devices:
            self._devices.pop(device.get_object_path())
