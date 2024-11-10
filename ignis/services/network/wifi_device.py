from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisGObject
from ._imports import NM
from .access_point import WifiAccessPoint, ActiveAccessPoint
from .constants import STATE


class WifiDevice(IgnisGObject):
    """
    A Wifi device.
    """

    def __init__(self, device: NM.DeviceWifi, client: NM.Client):
        super().__init__()
        self._device = device
        self._client = client
        self._access_points: list[WifiAccessPoint] = []

        self._client.connect(
            "notify::wireless-enabled", lambda *args: self.notify_all()
        )

        self._ap: ActiveAccessPoint = ActiveAccessPoint(self._device, self._client)

        self._device.connect("access-point-added", self.__sync_access_points)
        self._device.connect("access-point-removed", self.__sync_access_points)
        self._device.connect("notify::state", lambda x, y: self.notify("state"))
        self._device.connect(
            "notify::active-connection", lambda x, y: self.notify("is-connected")
        )

        self.__sync_access_points()

    @GObject.Property
    def access_points(self) -> list[WifiAccessPoint]:
        """
        - read-only

        A list of access points (Wi-FI networks).
        """
        return self._access_points

    @GObject.Property
    def ap(self) -> WifiAccessPoint:
        """
        - read-only

        The currently active access point.
        """
        return self._ap

    @GObject.Property
    def state(self) -> str | None:
        """
        - read-only

        The current state of the device or ``None`` if unknown.
        """
        return STATE.get(self._device.get_state(), None)

    @GObject.Property
    def is_connected(self) -> bool:
        """
        - read-only

        Whether the device is connected to a Wi-Fi network.
        """
        return (
            not not self._device.get_active_connection()
        )  # not not to convert to bool

    def scan(self) -> None:
        """
        Scan for Wi-Fi networks.
        """

        def finish(x, res) -> None:
            self._device.request_scan_finish(res)

        if self.state == "unavailable":
            return

        self._device.request_scan_async(None, finish)

    def __sync_access_points(self, *args) -> None:
        self._access_points = [
            WifiAccessPoint(point, self._client, self._device)
            for point in self._device.get_access_points()
        ]
        self.notify("access_points")
