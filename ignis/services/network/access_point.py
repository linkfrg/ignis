from gi.repository import GObject, GLib  # type: ignore
from ignis.gobject import IgnisGObject
from typing import Literal
from collections.abc import Callable
from ignis.app import IgnisApp
from .util import filter_connections
from ._imports import NM
from .wifi_connect_dialog import WifiConnectDialog
from .constants import WIFI_ICON_TEMPLATE

app = IgnisApp.get_default()


class WifiAccessPoint(IgnisGObject):
    """
    A Wi-Fi access point (Wi-Fi network).
    """

    def __init__(self, point: NM.AccessPoint, client: NM.Client, device: NM.DeviceWifi):
        super().__init__()

        self._client = client
        self._device = device
        self._point = point

        self._ssid: str | None = None
        self._connect_dialog: WifiConnectDialog | None = None
        self._connections: list[NM.Connection] = []

        self._state_changed_ids: dict[NM.ActiveConnection, int] = {}

        self._device.connect("state-changed", lambda *_: self.notify("is-connected"))
        self._client.connect(
            "notify::activating-connection", lambda *args: self.notify("icon-name")
        )

        self.__sync_connections()
        self._client.connect(
            "notify::connections", lambda *_: self.__sync_connections()
        )

        self._setup()

    def __sync_connections(self) -> None:
        self._connections = filter_connections(
            self._point,
            filter_connections(self._device, self._client.get_connections()),  # type: ignore
        )

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

    @GObject.Signal
    def removed(self):
        """
        Emitted when this access point is removed.
        """

    @GObject.Property
    def point(self) -> NM.AccessPoint:
        """
        - read-only

        An instance of ``NM.AccessPoint``.
        """
        return self._point

    @GObject.Property
    def bandwidth(self) -> int:
        """
        - read-only

        The channel bandwidth announced by the access point, in MHz.
        """
        return self._point.props.bandwidth

    @GObject.Property
    def bssid(self) -> str:
        """
        - read-only

        The BSSID of the access point.
        """
        return self._point.props.bssid

    @GObject.Property
    def frequency(self) -> int:
        """
        - read-only

        The frequency of the access point, in MHz.
        """
        return self._point.props.frequency

    @GObject.Property
    def last_seen(self) -> int:
        """
        - read-only

        The timestamp for the last time the access point was found in scan results.
        """
        return self._point.props.last_seen

    @GObject.Property
    def max_bitrate(self) -> int:
        """
        - read-only

        The maximum bit rate of the access point, in kbit/s.
        """
        return self._point.props.max_bitrate

    @GObject.Property
    def ssid(self) -> str | None:
        """
        - read-only

        The SSID of the access point, or ``None`` if it is not known.
        """
        return self._ssid

    @GObject.Property
    def strength(self) -> int:
        """
        - read-only

        The current signal strength of the access point, from 0 to 100.
        """
        return self._point.props.strength

    @GObject.Property
    def icon_name(self) -> str:
        """
        - read-only

        The current icon name for the access point. Depends on signal strength and current connection status.
        """
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
    def security(self) -> Literal["WPA1", "WPA2/WPA3"] | None:
        """
        - read-only

        The security protocol of the access point (``WPA1``, ``WPA2/WPA3``).
        """
        NM_80211ApSecurityFlags = getattr(NM, "80211ApSecurityFlags")
        if self._point.props.wpa_flags != NM_80211ApSecurityFlags.NONE:
            return "WPA1"
        elif self._point.props.rsn_flags != NM_80211ApSecurityFlags.NONE:
            return "WPA2/WPA3"
        else:
            return None

    @GObject.Property
    def psk(self) -> str | None:
        """
        - read-write

        The stored Pre-shared key (password) for the access point.
        ``None`` if there is no a saved psk for this access point.
        """
        for conn in self._connections:
            secrets: dict = conn.get_secrets("802-11-wireless-security").unpack()
            return secrets.get("802-11-wireless-security", {}).get("psk", None)
        else:
            return None

    @psk.setter
    def psk(self, value: str) -> None:
        for conn in self._connections:
            wireless_sec = NM.SettingWirelessSecurity.new()
            wireless_sec.set_property("psk", value)
            wireless_sec.set_property("key-mgmt", "wpa-psk")
            wireless_sec.set_secret_flags("psk", NM.SettingSecretFlags.NONE)
            conn.add_setting(wireless_sec)
            conn.commit_changes_async(
                True,
                None,
                lambda x, res, conn=conn: conn.commit_changes_finish(res),
            )

    @GObject.Property
    def is_connected(self) -> bool:
        """
        - read-only

        Whether the device is currently connected to this access point.
        """
        if self._device.get_state() != NM.DeviceState.ACTIVATED:
            return False

        if not self._device:
            return False

        ac = self._device.get_active_connection()
        if not ac:
            return False

        return self._point.connection_valid(ac.get_connection())

    def connect_to(self, password: str | None = None, on_state_changed: Callable | None = None) -> None:
        """
        Connect to this access point.

        Args
            password: Password to use. This has an effect only if the access point requires a password.
        """

        if len(self._connections) > 0:
            self.__connect_existing_connection(password, on_state_changed)
        else:
            self.__create_new_connection(password, on_state_changed)

    def connect_to_graphical(self) -> None:
        """
        Display a graphical dialog to connect to the access point.
        The dialog will be shown only if the access point requires a password.
        """
        self.connect_to(on_state_changed=self.__check_new_state)

    def disconnect_from(self) -> None:
        """
        Disconnect from this access point.
        """

        def finish(x, res) -> None:
            self._client.deactivate_connection_finish(res)

        self._client.deactivate_connection_async(
            self._device.get_active_connection(),
            None,
            finish,
        )

    def __connect_existing_connection(
        self, password: str | None = None, on_state_changed: Callable | None = None
    ) -> None:
        def finish(x, res) -> None:
            conn = self._client.activate_connection_finish(res)
            id_ = conn.connect(
                "state-changed",
                lambda x, new_state, reason: on_state_changed(x, new_state, reason)
                if on_state_changed
                else None,
            )
            self._state_changed_ids[conn] = id_

        if password is not None:
            self.psk = password
        for conn in self._connections:
            self._client.activate_connection_async(
                conn,
                self._device,
                self._point.get_path(),
                None,
                finish,
            )
            return

    def __create_new_connection(
        self, password: str | None = None, on_state_changed: Callable | None = None
    ) -> None:
        connection = NM.RemoteConnection()

        # WiFi settings
        wifi_setting = NM.SettingWireless.new()
        wifi_setting.props.ssid = GLib.Bytes.new(self.ssid.encode("utf-8"))
        connection.add_setting(wifi_setting)

        # WiFi security settings
        if self.security:
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
            conn = self._client.add_and_activate_connection_finish(res)
            id_ = conn.connect(
                "state-changed",
                lambda x, new_state, reason: on_state_changed(x, new_state, reason)
                if on_state_changed
                else None,
            )
            self._state_changed_ids[conn] = id_
            self.__sync_connections()

        self._client.add_and_activate_connection_async(
            connection,
            self._device,
            self._point.get_path(),
            None,
            finish,
        )

    def __check_new_state(self, conn, new_state, reason) -> None:
        if new_state != NM.ActiveConnectionState.ACTIVATING:
            id_ = self._state_changed_ids.pop(conn, None)
            if id_:
                conn.disconnect(id_)

        if reason == NM.ActiveConnectionStateReason.DEVICE_DISCONNECTED:
            self.__invoke_wifi_dialog()

        if (
            new_state == NM.ActiveConnectionState.ACTIVATED
            and self._connect_dialog is not None
        ):
            self._connect_dialog.destroy()

    def __invoke_wifi_dialog(self) -> None:
        if self._connect_dialog is None:
            self._connect_dialog = WifiConnectDialog(
                self, on_state_changed=self.__check_new_state
            )


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
