from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisGObject
from ._imports import NM
from .constants import STATE


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
