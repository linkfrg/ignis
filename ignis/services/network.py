from __future__ import annotations
import gi
import sys
from gi.repository import GObject, GLib  # type: ignore
from ignis.gobject import IgnisGObject
from typing import Iterator
from ignis.widgets import Widget
from ignis.exceptions import NetworkManagerNotFoundError


try:
    if "sphinx" not in sys.modules:
        gi.require_version("NM", "1.0")
    from gi.repository import NM  # type: ignore
except (ImportError, ValueError):
    raise NetworkManagerNotFoundError() from None


STATE = {
    NM.DeviceState.UNKNOWN: "unknown",
    NM.DeviceState.UNMANAGED: "unmanaged",
    NM.DeviceState.ACTIVATED: "activated",
    NM.DeviceState.DEACTIVATING: "deactivating",
    NM.DeviceState.FAILED: "failed",
    NM.DeviceState.UNAVAILABLE: "unavailable",
    NM.DeviceState.DISCONNECTED: "disconnected",
    NM.DeviceState.PREPARE: "prepare",
    NM.DeviceState.CONFIG: "config",
    NM.DeviceState.NEED_AUTH: "need_auth",
    NM.DeviceState.IP_CONFIG: "ip_config",
    NM.DeviceState.IP_CHECK: "ip_check",
    NM.DeviceState.SECONDARIES: "secondaries",
}

WIFI_ICON_TEMPLATE = "network-wireless-signal-{}-symbolic"


def get_devices(client: NM.Client, device_type: NM.DeviceType) -> Iterator[NM.Device]:
    for d in client.get_devices():
        if d.get_device_type() == device_type:
            yield d


class WifiConnectDialog(Widget.RegularWindow):
    """
    :meta private:
    """

    def __init__(self, access_point: WifiAccessPoint) -> None:
        self._password_entry = Widget.Entry(
            visibility=False, hexpand=True, on_accept=lambda x: self.__connect_to()
        )
        self._access_point = access_point
        super().__init__(
            resizable=False,
            width_request=400,
            height_request=200,
            namespace="wifi_connect",
            style="padding: 1rem;",
            child=Widget.Box(
                vertical=True,
                child=[
                    Widget.Box(
                        child=[
                            Widget.Icon(
                                icon_name="dialog-password",
                                pixel_size=48,
                                style="margin-bottom: 2rem; margin-right: 2rem; margin-left: 1rem; margin-top: 1rem;",
                            ),
                            Widget.Box(
                                vertical=True,
                                spacing=20,
                                child=[
                                    Widget.Label(
                                        label="Authentication required by Wi-Fi network",
                                        style="font-size: 1.1rem;",
                                    ),
                                    Widget.Label(
                                        label=f'Passwords or encryption keys are required to access the Wi-Fi network "{access_point.ssid}".',
                                        wrap=True,
                                        max_width_chars=30,
                                        style="font-weight: normal;",
                                    ),
                                ],
                            ),
                        ]
                    ),
                    Widget.Box(
                        child=[Widget.Label(label="Password"), self._password_entry],
                        spacing=10,
                        style="margin-top: 1rem;",
                    ),
                    Widget.CheckButton(
                        label="Show password",
                        active=True,
                        on_toggled=lambda x,
                        active: self._password_entry.set_visibility(not active),
                        style="margin-left: 5.5rem; margin-top: 0.5rem;",
                    ),
                    Widget.Box(
                        vexpand=True,
                        valign="end",
                        halign="end",
                        spacing=10,
                        child=[
                            Widget.Button(
                                label="Cancel",
                                on_click=lambda x: self.unrealize(),
                            ),
                            Widget.Button(
                                sensitive=self._password_entry.bind(
                                    "text", lambda value: len(value) >= 8
                                ),
                                label="Connect",
                                on_click=lambda x: self.__connect_to(),
                            ),
                        ],
                    ),
                ],
            ),
        )

    def __connect_to(self) -> None:
        if len(self._password_entry.text) >= 8:
            self._access_point.connect_to(self._password_entry.text)
            self.unrealize()


class WifiAccessPoint(IgnisGObject):
    """
    A Wi-Fi access point (Wi-Fi network).

    Properties:
        - **point** (``NM.AccessPoint``, read-only): An instance of ``NM.AccessPoint``. You typically shouldn't use this property.
        - **bandwidth** (``int``, read-only): The channel bandwidth announced by the access point, in MHz.
        - **bssid** (``str``, read-only): The BSSID of the access point.
        - **frequency** (``int``, read-only): The frequency of the access point, in MHz.
        - **last_seen** (``int``, read-only): The timestamp for the last time the access point was found in scan results.
        - **max_bitrate** (``int``, read-only): The maximum bit rate of the access point, in kbit/s.
        - **ssid** (``str | None``, read-only): The SSID of the access point, or ``None`` if it is not known.
        - **strength** (``int``, read-only): The current signal strength of the access point, from 0 to 100.
        - **icon_name** (``str``, read-only): The current icon name for the access point. Depends on signal strength and current connection status.
        - **requires_password** (``bool``, read-only): Whether the access point requires a password to connect.
        - **is_connected** (``bool``, read-only): Whether the device is currently connected to this access point.

    Raises:
        NetworkManagerNotFoundError: If Network Manager is not found.
    """

    def __init__(self, point: NM.AccessPoint, client: NM.Client, device: NM.DeviceWifi):
        super().__init__()

        self._client = client
        self._device = device
        self._point = point

        self._ssid: str | None = None

        self._device.connect(
            "notify::active-access-point", lambda x, y: self.notify("is-connected")
        )
        self._client.connect(
            "notify::activating-connection", lambda *args: self.notify("icon-name")
        )

        self._setup()

    def _setup(self) -> None:
        """
        :meta private:
        """
        self._point.connect(
            "notify::strength",
            lambda *args: self.notify_list("strength", "icon-name"),
        )

        self._ssid = self.__get_ssid()

    def __get_ssid(self) -> str | None:
        ssid = self._point.props.ssid
        if not ssid:
            return None

        data = ssid.get_data()
        if not data:
            return None

        return NM.utils_ssid_to_utf8(data)

    @GObject.Property
    def point(self) -> NM.AccessPoint:
        return self._point

    @GObject.Property
    def bandwidth(self) -> int:
        return self._point.props.bandwidth

    @GObject.Property
    def bssid(self) -> str:
        return self._point.props.bssid

    @GObject.Property
    def frequency(self) -> int:
        return self._point.props.frequency

    @GObject.Property
    def last_seen(self) -> int:
        return self._point.props.last_seen

    @GObject.Property
    def max_bitrate(self) -> int:
        return self._point.props.max_bitrate

    @GObject.Property
    def ssid(self) -> str | None:
        return self._ssid

    @GObject.Property
    def strength(self) -> int:
        return self._point.props.strength

    @GObject.Property
    def icon_name(self) -> str:
        ac = self._client.get_activating_connection()
        if ac:
            if ac.get_state() == NM.ActiveConnectionState.ACTIVATING:
                return "network-wireless-acquiring-symbolic"

        if self.strength > 80:
            return WIFI_ICON_TEMPLATE.format("excellent")
        elif self.strength > 60:
            return WIFI_ICON_TEMPLATE.format("good")
        elif self.strength > 40:
            return WIFI_ICON_TEMPLATE.format("ok")
        elif self.strength > 20:
            return WIFI_ICON_TEMPLATE.format("weak")
        elif self.strength > 0:
            return WIFI_ICON_TEMPLATE.format("none")
        else:
            return "network-wireless-offline-symbolic"

    @GObject.Property
    def requires_password(self) -> bool:
        NM_80211ApFlags = getattr(NM, "80211ApFlags")
        privacy_flag = NM_80211ApFlags.PRIVACY
        return self._point.get_flags() == privacy_flag

    @GObject.Property
    def is_connected(self) -> bool:
        if not self._device:
            return False

        ap = self._device.get_active_access_point()
        if not ap:
            return False

        return ap.props.bssid == self.bssid

    def connect_to(self, password: str | None = None) -> None:
        """
        Connect to this access point.

        Args
            password (``str``, optional): Password to use. This has an effect only if the access point requires a password.
        """
        connection = NM.RemoteConnection()

        # WiFi settings
        wifi_setting = NM.SettingWireless.new()
        wifi_setting.props.ssid = GLib.Bytes.new(self.ssid.encode("utf-8"))
        connection.add_setting(wifi_setting)

        # WiFi security settings
        if self.requires_password:
            wifi_sec_setting = NM.SettingWirelessSecurity.new()
            wifi_sec_setting.set_property("key-mgmt", "wpa-psk")
            wifi_sec_setting.set_property("psk", password)
            connection.add_setting(wifi_sec_setting)

        # IP4 settings
        ip4_setting = NM.SettingIP4Config.new()
        ip4_setting.set_property("method", "auto")
        connection.add_setting(ip4_setting)

        # IP6 settings
        ip6_setting = NM.SettingIP6Config.new()
        ip6_setting.set_property("method", "auto")
        connection.add_setting(ip6_setting)

        # Connection settings
        connection_setting = NM.SettingConnection.new()
        connection_setting.set_property("id", self.ssid)
        connection_setting.set_property("type", "802-11-wireless")
        connection_setting.set_property("uuid", NM.utils_uuid_generate())
        connection_setting.set_property("interface-name", self._device.get_iface())
        connection.add_setting(connection_setting)

        # Proxy settings
        proxy_setting = NM.SettingProxy.new()
        connection.add_setting(proxy_setting)

        def finish(x, res) -> None:
            self._client.add_and_activate_connection_finish(res)

        self._client.add_and_activate_connection_async(
            connection,
            self._device,
            self._point.get_path(),
            None,
            finish,
        )

    def connect_to_graphical(self) -> None:
        """
        Display a graphical dialog to connect to the access point.
        The dialog will be shown only if the access point requires a password.
        """
        if self.requires_password:
            WifiConnectDialog(self)
        else:
            self.connect_to()


class ActiveAccessPoint(WifiAccessPoint):
    """
    :meta private:
    """

    def __init__(self, device: NM.DeviceWifi, client: NM.Client):
        super().__init__(NM.AccessPoint(), client, device)
        self._device = device
        self._device.connect("notify::active-access-point", lambda *args: self.__sync())
        self.__sync()

    def __sync(self) -> None:
        ap = self._device.get_active_access_point()
        if ap:
            self._point = ap
            self._setup()
        else:
            self._point = NM.AccessPoint()

        self.notify_all()


class WifiDevice(IgnisGObject):
    """
    A Wifi device.

    Properties:
        - **access_points** (list[:class:`~ignis.services.network.WifiAccessPoint`], read-only): A list of access points (Wi-FI networks).
        - **ap** (:class:`~ignis.services.network.WifiAccessPoint`, read-only): The currently active access point.
        - **state** (``str | None``, read-only): The current state of the device or ``None`` if unknown.
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
        return self._access_points

    @GObject.Property
    def ap(self) -> WifiAccessPoint:
        return self._ap

    @GObject.Property
    def state(self) -> str | None:
        return STATE.get(self._device.get_state(), None)

    @GObject.Property
    def is_connected(self) -> bool:
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


class Wifi(IgnisGObject):
    """
    Class for controlling Wi-Fi devices.

    Properties:
        - **devices** (:class:`~ignis.services.network.WifiDevice`, read-only): A list of Wi-Fi devices.
        - **is_connected** (``bool``, read-only): Whether at least one Wi-Fi device is connected to the network.
        - **icon_name** (``str``, read-only): The icon name of the first device in the list.
        - **enabled** (``bool``, read-only): Whether Wi-Fi is enabled.
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
        return self._devices

    @GObject.Property
    def is_connected(self) -> bool:
        for i in self._devices:
            if i.is_connected:
                return True
        return False

    @GObject.Property
    def icon_name(self) -> str:
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


class EthernetDevice(IgnisGObject):
    """
    Ethernet device.

    Properties:
        - **carrier** (``bool``, read-only): Whether the device has a carrier.
        - **perm_hw_address** (``str``, read-only): The permanent hardware (MAC) address of the device.
        - **speed** (``int``, read-only): The speed of the device.
        - **state** (``str | None``, read-only): Current state of the device or ``None`` if unknown.
        - **is_connected** (``bool``, read-only): Whether the device is connected to the network.
        - **name** (``str | None``, read-only): The name of the connection or ``None`` if unknown.
    """

    def __init__(self, device: NM.DeviceEthernet, client: NM.Client):
        super().__init__()
        self._device = device
        self._client = client
        self._name: str | None = None
        self._is_connected: bool = False

        self._connection: NM.RemoteConnection = (
            self._device.get_available_connections()[0]
        )
        setting_connection: NM.SettingConnection = (
            self._connection.get_setting_connection()
        )
        self._name = setting_connection.props.id

        self._device.connect("notify::active-connection", self.__update_is_connected)
        self.__update_is_connected()

    @GObject.Property
    def carrier(self) -> bool:
        return self._device.props.carrier

    @GObject.Property
    def perm_hw_address(self) -> str:
        return self._device.props.perm_hw_address

    @GObject.Property
    def speed(self) -> int:
        return self._device.props.speed

    @GObject.Property
    def state(self) -> str | None:
        return STATE.get(self._device.get_state(), None)

    @GObject.Property
    def is_connected(self) -> bool:
        return self._is_connected

    @GObject.Property
    def name(self) -> str | None:
        return self._name

    def connect_to(self) -> None:
        """
        Connect this Ethernet device to the network.
        """

        def finish(x, res) -> None:
            self._client.activate_connection_finish(res)

        self._client.activate_connection_async(
            self._connection,
            self._device,
            None,
            None,
            finish,
        )

    def disconnect_from(self) -> None:
        """
        Disconnect this Ethernet device from the network.
        """
        if not self.is_connected:
            return

        def finish(x, res) -> None:
            self._client.deactivate_connection_finish(res)

        self._client.deactivate_connection_async(
            self._device.get_active_connection(),
            None,
            finish,
        )

    def __update_is_connected(self, *args) -> None:
        if not self._device.get_active_connection():
            self._is_connected = False
        else:
            self._is_connected = True
        self.notify("is-connected")


class Ethernet(IgnisGObject):
    """
    Class for controlling Ethernet devices.

    Properties:
        - **devices** (:class:`~ignis.services.network.EthernetDevice`, read-only): A list of Ethernet devices.
        - **is_connected** (``bool``, read-only): Whether at least one Ethernet device is connected to the network.
        - **icon_name** (``str``, read-only): The general icon name for all devices, depends on ``is_connected`` property.
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
        return self._devices

    @GObject.Property
    def is_connected(self) -> bool:
        for i in self.devices:
            if i.is_connected:
                return True
        return False

    @GObject.Property
    def icon_name(self) -> str:
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


class NetworkService(IgnisGObject):
    """
    A Network service. Uses ``NetworkManager``.

    Properties:
        - **wifi** (:class:`~ignis.services.network.Wifi`, read-only): The Wi-Fi object.
        - **ethernet** (:class:`~ignis.services.network.Ethernet`, read-only): The Ethernet device object.
    """

    def __init__(self):
        super().__init__()
        self._client = NM.Client.new(None)
        self._wifi = Wifi(self._client)
        self._ethernet = Ethernet(self._client)

    @GObject.Property
    def wifi(self) -> Wifi:
        return self._wifi

    @GObject.Property
    def ethernet(self) -> Ethernet:
        return self._ethernet
