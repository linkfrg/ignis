from gi.repository import GObject, GLib  # type: ignore
from ignis.gobject import IgnisGObject
from .ethernet_device import EthernetDevice
from ._imports import NM
from .util import get_devices


class Ethernet(IgnisGObject):
    """
    The class for controlling Ethernet devices.
    """

    def __init__(self, client: NM.Client):
        super().__init__()
        self._client = client
        self._devices: list[EthernetDevice] = []
        self._client.connect(
            "notify::all-devices",
            lambda *args: GLib.timeout_add_seconds(1, self.__sync),
        )
        self.__sync()

    @GObject.Property
    def devices(self) -> list[EthernetDevice]:
        """
        - read-only

        A list of Ethernet devices.
        """
        return self._devices

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

    def __sync(self) -> None:
        self._devices = []
        for device in get_devices(self._client, NM.DeviceType.ETHERNET):
            self.__add_device(device)  # type: ignore

        self.notify_all()

    def __add_device(self, device: NM.DeviceEthernet) -> None:
        if len(device.get_available_connections()) == 0:
            return

        dev = EthernetDevice(device, self._client)
        dev.connect(
            "notify::is-connected",
            lambda x, y: self.notify_list("is-connected", "icon-name"),
        )
        self._devices.append(dev)
