from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisGObject
from .ethernet_device import EthernetDevice
from ._imports import NM


class Ethernet(IgnisGObject):
    """
    The class for controlling Ethernet devices.
    """

    def __init__(self, client: NM.Client):
        super().__init__()
        self._client = client
        self._devices: dict[NM.Device, EthernetDevice] = {}

        self._client.connect("device-added", self.__add_device)
        self._client.connect("device-removed", self.__remove_device)

        for device in self._client.get_devices():
            self.__add_device(None, device, False)

    @GObject.Signal(arg_types=(EthernetDevice,))
    def new_device(self, *args):
        """
        Emitted when a new Ethernet device is added.

        Args:
            device (:class:`~ignis.services.network.WifiDevice`): An instance of the device.
        """

    @GObject.Property
    def devices(self) -> list[EthernetDevice]:
        """
        - read-only

        A list of Ethernet devices.
        """
        return list(self._devices.values())

    @GObject.Property
    def is_connected(self) -> bool:
        """
        - read-only

        Whether at least one Ethernet device is connected to the network.
        """
        for i in self.devices:
            if i.is_connected:
                return True
        return False

    @GObject.Property
    def icon_name(self) -> str:
        """
        - read-only

        The general icon name for all devices, depends on ``is_connected`` property.
        """
        if self.is_connected:
            return "network-wired-symbolic"
        else:
            return "network-wired-disconnected-symbolic"

    def __add_device(self, client, device: NM.Device, emit: bool = True) -> None:
        if device.get_device_type() != NM.DeviceType.ETHERNET:
            return

        if len(device.get_available_connections()) == 0:
            return

        obj = EthernetDevice(device, self._client)  # type: ignore
        obj.connect(
            "notify::is-connected",
            lambda x, y: self.notify_list("is-connected", "icon-name"),
        )
        self._devices[device] = obj

        if emit:
            self.emit("new-device", obj)
            self.notify("devices")

    def __remove_device(self, client, device: NM.DeviceEthernet) -> None:
        if device.get_device_type() != NM.DeviceType.ETHERNET:
            return

        obj = self._devices.pop(device)
        obj.emit("removed")
        self.notify("devices")
