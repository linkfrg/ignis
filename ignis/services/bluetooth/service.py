from gi.repository import GObject  # type: ignore
from ignis.base_service import BaseService
from ._imports import GnomeBluetooth
from .device import BluetoothDevice
from .constants import ADAPTER_STATE


class BluetoothService(BaseService):
    __gsignals__ = {
        "device-added": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (BluetoothDevice,)),
    }

    def __init__(self) -> None:
        super().__init__()

        self._client = GnomeBluetooth.Client.new()
        self._devices: dict[str, BluetoothDevice] = {}

        self._client.connect("device-added", self.__add_device)
        self._client.connect("device-added", self.__remove_device)

        for gdevice in self._client.get_devices():
            self.__add_device(None, gdevice)  # type: ignore

    @GObject.Property
    def devices(self) -> list[BluetoothDevice]:
        return list(self._devices.values())

    @GObject.Property
    def powered(self) -> bool:
        return self._client.props.default_adapter_powered

    @powered.setter
    def powered(self, value: bool) -> None:
        self._client.props.default_adapter_powered = value

    @GObject.Property
    def state(self) -> str:
        return ADAPTER_STATE.get(self._client.props.default_adapter_state, "absent")

    def __add_device(self, x, gdevice: GnomeBluetooth.Device) -> None:
        device = BluetoothDevice(self._client, gdevice)
        self._devices[gdevice.get_object_path()] = device
        self.emit("device-added", device)
        self.notify("devices")

    def __remove_device(self, x, object_path: str) -> None:
        if object_path not in self._devices:
            return

        device = self._devices.pop(object_path)
        device.emit("removed")
        self.notify("devices")