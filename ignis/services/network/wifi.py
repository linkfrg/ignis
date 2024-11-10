from gi.repository import GObject, GLib  # type: ignore
from ignis.gobject import IgnisGObject
from ._imports import NM
from .wifi_device import WifiDevice
from .util import get_devices


class Wifi(IgnisGObject):
    """
    The class for controlling Wi-Fi devices.
    """

    def __init__(self, client: NM.Client):
        super().__init__()
        self._client = client
        self._devices: list[WifiDevice] = []
        self._client.connect(
            "notify::all-devices",
            lambda *args: GLib.timeout_add_seconds(1, self.__sync),
        )
        self._client.connect(
            "notify::wireless-enabled",
            lambda *args: self.notify_list("enabled", "icon-name", "is-connected"),
        )
        self.__sync()

    @GObject.Property
    def devices(self) -> list[WifiDevice]:
        """
        - read-only

        A list of Wi-Fi devices.
        """
        return self._devices

    @GObject.Property
    def is_connected(self) -> bool:
        """
        - read-only

        Whether at least one Wi-Fi device is connected to the network.
        """
        for i in self._devices:
            if i.is_connected:
                return True
        return False

    @GObject.Property
    def icon_name(self) -> str:
        """
        - read-only

        The icon name of the first device in the list.
        """
        result = None
        for i in self._devices:
            if i.ap.icon_name != "network-wireless-offline-symbolic":
                result = i.ap.icon_name

        if not result:
            return "network-wireless-offline-symbolic"
        else:
            return result

    @GObject.Property
    def enabled(self) -> bool:
        """
        - read-write

        Whether Wi-Fi is enabled.
        """
        return self._client.wireless_get_enabled()

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._client.wireless_set_enabled(value)

    def __sync(self) -> None:
        self._devices = []
        for device in get_devices(self._client, NM.DeviceType.WIFI):
            self.__add_device(device)  # type: ignore

        self.notify_all()

    def __add_device(self, device: NM.DeviceWifi) -> None:
        dev = WifiDevice(device, self._client)
        dev.ap.connect(
            "notify::icon-name",
            lambda x, y: self.notify("icon-name"),
        )
        dev.ap.connect(
            "notify::is-connected",
            lambda x, y: self.notify("is-connected"),
        )
        self._devices.append(dev)
