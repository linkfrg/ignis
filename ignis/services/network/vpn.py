from gi.repository import GObject, GLib  # type: ignore
from ignis.gobject import IgnisGObject
from ._imports import NM


class VpnConnection(IgnisGObject):
    """
    A VPN connection.
    """

    def __init__(self, connection: NM.RemoteConnection, client: NM.Client):
        super().__init__()
        self._connection = connection
        self._client = client

        active_uuids = [
            conn.get_uuid() for conn in self._client.get_active_connections()
        ]
        self._is_connected: bool = connection.get_uuid() in active_uuids

        self._client.connect("notify::active-connections", self.__update_is_connected)
        self.__update_is_connected()

    @GObject.Property
    def is_connected(self) -> bool:
        """
        - read-only

        Whether the device is connected to the network.
        """
        return self._is_connected

    @GObject.Property
    def name(self) -> str | None:
        """
        - read-only

        The id (name) of the vpn connection or ``None`` if unknown.
        """
        return self._connection.get_id()

    def toggle_connection(self) -> None:
        """
        Toggle this VPN depending on it's `is_connected` property
        """
        if self.is_connected:
            self.disconnect_from()
        else:
            self.connect_to()

    def connect_to(self) -> None:
        """
        Connect to this VPN.
        """

        def finish(x, res) -> None:
            self._client.activate_connection_finish(res)

        self._client.activate_connection_async(
            self._connection,
            None,
            None,
            None,
            finish,
        )

    def disconnect_from(self) -> None:
        """
        Disconnect from this VPN.
        """

        def finish(x, res) -> None:
            self._client.deactivate_connection_finish(res)

        for conn in self._client.get_active_connections():
            if conn.get_uuid() == self._connection.get_uuid():
                self._client.deactivate_connection_async(
                    conn,
                    None,
                    finish,
                )

    def __update_is_connected(self, *args) -> None:
        active_uuids = [
            conn.get_uuid() for conn in self._client.get_active_connections()
        ]
        self._is_connected = self._connection.get_uuid() in active_uuids

        self.notify("is-connected")


class Vpn(IgnisGObject):
    """
    The class for controlling VPN connections.
    """

    def __init__(self, client: NM.Client):
        super().__init__()
        self._client = client
        self._connections: list[VpnConnection] = []
        self._active_vpn_connections: list[VpnConnection] = []
        self._client.connect(
            "notify::connections",
            lambda *args: GLib.timeout_add_seconds(1, self.__sync),
        )
        self._client.connect(
            "notify::active-connections",
            lambda *args: GLib.timeout_add_seconds(1, self.__sync),
        )
        self.__sync()

    @GObject.Property
    def connections(self) -> list[VpnConnection]:
        """
        - read-only

        A list of VPN connections.
        """
        return self._connections

    @GObject.Property
    def active_vpn_id(self) -> str | None:
        """
        - read-only

        The id (name) of the first active vpn connection.
        """
        if not self.is_connected:
            return None
        else:
            return self._active_vpn_connections[0].name

    @GObject.Property
    def is_connected(self) -> bool:
        """
        - read-only

        Whether at least one VPN connection is active.
        """
        return len(self._active_vpn_connections) != 0

    @GObject.Property
    def icon_name(self) -> str:
        """
        - read-only

        The general icon name for all vpn connections, depends on ``is_connected`` property.
        """
        if self.is_connected:
            return "network-vpn-symbolic"
        else:
            return "network-vpn-disconnected-symbolic"

    def __sync(self) -> None:
        def filter_conn(df):
            return [
                VpnConnection(conn, self._client)
                for conn in df()
                if conn.get_connection_type() == "vpn"
            ]

        self._connections = filter_conn(self._client.get_connections)

        self._active_vpn_connections = filter_conn(self._client.get_active_connections)

        for connection in self._active_vpn_connections:
            self.__add_connection(connection)  # type: ignore

        self.notify_all()

    def __add_connection(self, connection: VpnConnection) -> None:
        connection.connect(
            "notify::is-connected",
            lambda x, y: self.notify_list("is-connected", "icon-name"),
        )
