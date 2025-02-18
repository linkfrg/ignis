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
        self._access_points: dict[str, WifiAccessPoint] = {}  # bssid: WifiAccessPoint

        self._client.connect(
            "notify::wireless-enabled", lambda *args: self.notify_all()
        )

        self._ap: ActiveAccessPoint = ActiveAccessPoint(self._device, self._client)

        self._device.connect("access-point-added", self.__add_access_point)
        self._device.connect("access-point-removed", self.__remove_access_point)

        self._device.connect("notify::state", lambda x, y: self.notify("state"))
        self._device.connect(
            "notify::active-connection", lambda x, y: self.notify("is-connected")
        )

        for i in self._device.get_access_points():
            self.__add_access_point(None, i, False)

    @GObject.Signal
    def removed(self):
        """
        Emitted when this Wi-Fi device is removed.
        """

    @GObject.Signal(arg_types=(WifiAccessPoint,))
    def new_access_point(self, *args):
        """
        Emitted when a new access point is added.

        Args:
            access_point (:class:`~ignis.services.network.WifiAccessPoint`): An instance of the access point.
        """

    @GObject.Property
    def access_points(self) -> list[WifiAccessPoint]:
        """
        - read-only

        A list of access points (Wi-FI networks).
        """
        return list(self._access_points.values())

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
        return bool(self._device.get_active_connection())

    async def scan(self) -> None:
        """
        Scan for Wi-Fi networks.
        """

        if self.state == "unavailable":
            return

        await self._device.request_scan_async()  # type: ignore

    def __add_access_point(
        self, device, access_point: NM.AccessPoint, emit: bool = True
    ) -> None:
        if access_point.props.bssid in self._access_points:
            return

        obj = WifiAccessPoint(access_point, self._client, self._device)
        self._access_points[access_point.props.bssid] = obj

        if emit:
            self.emit("new-access-point", obj)
            self.notify("access-points")

    def __remove_access_point(self, device, access_point: NM.AccessPoint) -> None:
        try:
            obj = self._access_points.pop(access_point.props.bssid)
            obj.emit("removed")
            self.notify("access-points")
        except KeyError:
            pass
