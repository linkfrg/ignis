import gi
from gi.repository import GObject, GLib
from ignis.gobject import IgnisGObject
from typing import List
from ignis.widgets import Widget
from ignis.exceptions import NetworkManagerNotFoundError


try:
    gi.require_version("NM", "1.0")
    from gi.repository import NM
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


def get_device(client: NM.Client, device_type: NM.DeviceType):
    active = None
    latest = None
    for d in client.get_devices():
        if d.get_device_type() == device_type:
            if not d.get_state() == NM.DeviceState.UNAVAILABLE:
                active = d
            else:
                latest = d

    if active:
        return active
    else:
        return latest


class WifiConnectDialog(Widget.RegularWindow):
    """
    :meta private:
    """

    def __init__(self, access_point) -> None:
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
        - **ssid** (``str``, read-only): The SSID of the access point, or ``None`` if it is not known.
        - **strength** (``int``, read-only): The current signal strength of the access point, from 0 to 100.
        - **icon_name** (``str``, read-only): The current icon name for the access point. Depends on signal strength and current connection status.
        - **requires_password** (``bool``, read-only): Whether the access point requires a password to connect.
        - **is_connected** (``bool``, read-only): Whether the device is currently connected to this access point.
    """

    def __init__(self, point: NM.AccessPoint, client: NM.Client, device: NM.DeviceWifi):
        super().__init__()

        self.__client = client
        self.__device = device
        self._point = point

        self._setup()

    def _setup(self) -> None:
        """
        :meta private:
        """
        self._point.connect(
            "notify::strength",
            lambda *args: (self.notify("strength"), self.notify("icon-name")),
        )
        if self.__device:
            self.__device.connect(
                "notify::active-access-point", lambda x, y: self.notify("is-connected")
            )

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
    def ssid(self) -> str:
        if self._point.props.ssid:
            return NM.utils_ssid_to_utf8(self._point.props.ssid.get_data())

    @GObject.Property
    def strength(self) -> int:
        return self._point.props.strength

    @GObject.Property
    def icon_name(self) -> str:
        ac = self.__client.get_activating_connection()
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
        if not self.__device:
            return False

        ap = self.__device.get_active_access_point()
        if not ap:
            return False

        return ap.props.bssid == self.bssid

    def connect_to(self, password: str = None) -> None:
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
        connection_setting.set_property("interface-name", self.__device.get_iface())
        connection.add_setting(connection_setting)

        # Proxy settings
        proxy_setting = NM.SettingProxy.new()
        connection.add_setting(proxy_setting)

        self.__client.add_and_activate_connection_async(
            connection,
            self.__device,
            self._point.get_path(),
            None,
            lambda x, res: self.__client.add_and_activate_connection_finish(res),
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

    def __init__(self, client: NM.Client):
        self.__client = client
        super().__init__(NM.AccessPoint(), client, None)
        self._sync_device()

    def _sync_device(self) -> None:
        """
        :meta private:
        """
        self.__device = get_device(self.__client, NM.DeviceType.WIFI)
        if self.__device:
            self.__device.connect(
                "notify::active-access-point",
                lambda *args: self.__sync_ap(),
            )
        self.__sync_ap()

    def __sync_ap(self) -> None:
        if not self.__device:
            self._point = NM.AccessPoint()
            self.notify_all()
            return

        ap = self.__device.get_active_access_point()
        if ap:
            self._setup()
            self._point = ap
        else:
            self._point = NM.AccessPoint()

        self.notify_all()


class Wifi(IgnisGObject):
    """
    A Wifi device.

    Properties:
        - **access_points** (List[:class:`~ignis.services.network.WifiAccessPoint`], read-only): List of access points (Wi-FI networks).
        - **ap** (:class:`~ignis.services.network.WifiAccessPoint`, read-only): Current active access point.
        - **state** (str, read-only): Current state of the device.
        - **enabled** (bool, read-write): Whether Wi-FI is enabled.
    """

    def __init__(self, client: NM.Client):
        super().__init__()
        self.__client = client
        self._access_points = []

        self.__client.connect(
            "notify::wireless-enabled", lambda *args: self.notify_all()
        )
        self.__client.connect(
            "notify::activating-connection", lambda *args: self.ap.notify("icon-name")
        )

        self._ap = ActiveAccessPoint(self.__client)
        self._sync()

    @GObject.Property
    def access_points(self) -> List[WifiAccessPoint]:
        return self._access_points

    @GObject.Property
    def ap(self) -> WifiAccessPoint:
        return self._ap

    @GObject.Property
    def state(self) -> str:
        if self.__device:
            return STATE.get(self.__device.get_state(), None)
        else:
            return "unavailable"

    @GObject.Property
    def enabled(self) -> bool:
        return self.__client.wireless_get_enabled()

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self.__client.wireless_set_enabled(value)

    def scan(self) -> None:
        """
        Scan for Wi-Fi networks.
        """
        if self.__device and self.state != "unavailable":
            self.__device.request_scan_async(
                None, lambda x, result: self.__device.request_scan_finish(result)
            )

    def _sync(self) -> None:
        """
        :meta private:
        """
        self.__device = get_device(client=self.__client, device_type=NM.DeviceType.WIFI)
        if self.__device:
            self.__device.connect("access-point-added", self.__sync_access_points)
            self.__device.connect("access-point-removed", self.__sync_access_points)
            self.__device.connect("notify::state", lambda x, y: self.notify("state"))

            self.__sync_access_points()
            self._ap._sync_device()

        self.notify_all()

    def __sync_access_points(self, *args) -> None:
        self._access_points = [
            WifiAccessPoint(point, self.__client, self.__device)
            for point in self.__device.get_access_points()
        ]
        self.notify("access_points")


class Ethernet(IgnisGObject):
    """
    Ethernet device.

    Properties:
        - **carrier** (``bool``, read-only): Whether the device has a carrier.
        - **perm_hw_address** (``str``, read-only): The permanent hardware (MAC) address of the device.
        - **speed** (``str``, read-only): The speed of the device.
        - **state** (str, read-only): Current state of the device.
    """

    def __init__(self, client: NM.Client):
        super().__init__()
        self.__client = client
        self._sync()

    def _sync(self) -> None:
        """
        :meta private:
        """
        self.__device = get_device(
            client=self.__client, device_type=NM.DeviceType.ETHERNET
        )
        self.notify_all()

    @GObject.Property
    def carrier(self) -> bool:
        return self.__device.props.carrier

    @GObject.Property
    def perm_hw_address(self) -> str:
        return self.__device.props.perm_hw_address

    @GObject.Property
    def speed(self) -> bool:
        return self.__device.props.speed

    @GObject.Property
    def state(self) -> str:
        if self.__device:
            return STATE.get(self.__device.get_state(), None)
        else:
            return "unavailable"


class NetworkService(IgnisGObject):
    """
    A Network service. Uses ``NetworkManager``.

    Properties:
        - **wifi** (:class:`~ignis.services.network.Wifi`, read-only): The WiFi device object.
        - **ethernet** (:class:`~ignis.services.network.Ethernet`, read-only): The Ethernet device object.
    """

    def __init__(self):
        super().__init__()
        self.__client = NM.Client.new(None)
        self.__client.connect(
            "notify::all-devices",
            lambda *args: GLib.timeout_add_seconds(2, self.__sync),
        )

        self._wifi = Wifi(self.__client)
        self._ethernet = Ethernet(self.__client)

    @GObject.Property
    def wifi(self) -> Wifi:
        return self._wifi

    @GObject.Property
    def ethernet(self) -> Ethernet:
        return self._ethernet

    def __sync(self) -> None:
        self._wifi._sync()
        self._ethernet._sync()
