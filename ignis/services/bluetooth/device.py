from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisGObject
from ._imports import GnomeBluetooth


class BluetoothDevice(IgnisGObject):
    """
    A Bluetooth device.

    Signals:
        - **removed** (): Emitted when the device has been removed.

    Properties:
        - **gdevice** (``GnomeBluetooth.Device``, read-only): The instance of ``GnomeBluetooth.Device`` for this device.
        - **address** (``str``, read-only): The Bluetooth device address of the device.
        - **alias** (``str``, read-only): The name alias for the device.
        - **battery_level** (``int``, read-only): The current battery level of the device (if available).
        - **battery_percentage** (``float``, read-only): The current battery percentage of the device (if available).
        - **connectable** (``bool``, read-only): Whether it is possible to connect to the device.
        - **connected** (``bool``, read-only): Whether the device is currently connected.
        - **icon_name** (``str``, read-only): The current icon name of the device.
        - **name** (``str``, read-only): The complete device name. It is better to use the ``alias`` property when displaying the device name.
        - **paired** (``bool``, read-only): Whether the device is paired.
        - **trusted** (``bool``, read-only): Whether the remote is seen as trusted.
        - **device_type** (``str``, read-only): The type of the device, e.g., ``"mouse"``, ``"speakers"``.

    For more device types, see `GnomeBluetooth.Type <https://lazka.github.io/pgi-docs/index.html#GnomeBluetooth-3.0/flags.html#GnomeBluetooth.Type>`_.
    """

    __gsignals__ = {
        "removed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(
        self, client: GnomeBluetooth.Client, gdevice: GnomeBluetooth.Device
    ) -> None:
        super().__init__()

        self._client = client
        self._gdevice = gdevice

        for prop_name in [
            "address",
            "alias",
            "battery-level",
            "battery-percentage",
            "connected",
            "name",
            "paired",
            "trusted",
        ]:
            gdevice.connect(
                f"notify::{prop_name}",
                lambda x, y, prop_name=prop_name: self.notify(prop_name),
            )
        gdevice.connect("notify::icon", lambda x, y: self.notify("icon-name"))

    @GObject.Property
    def gdevice(self) -> GnomeBluetooth.Device:
        return self._gdevice

    @GObject.Property
    def address(self) -> str:
        return self._gdevice.props.address

    @GObject.Property
    def alias(self) -> str:
        return self._gdevice.props.alias

    @GObject.Property
    def battery_level(self) -> int:
        return self._gdevice.props.battery_level

    @GObject.Property
    def battery_percentage(self) -> float:
        return self._gdevice.props.battery_percentage

    @GObject.Property
    def connectable(self) -> bool:
        return self._gdevice.props.connectable

    @GObject.Property
    def connected(self) -> bool:
        return self._gdevice.props.connected

    @GObject.Property
    def icon_name(self) -> str:
        return self._gdevice.props.icon

    @GObject.Property
    def name(self) -> str:
        return self._gdevice.props.name

    @GObject.Property
    def paired(self) -> bool:
        return self._gdevice.props.paired

    @GObject.Property
    def trusted(self) -> bool:
        return self._gdevice.props.trusted

    @GObject.Property
    def device_type(self) -> str:
        return GnomeBluetooth.type_to_string(self._gdevice.props.type)  # type: ignore

    def __connect_service(self, connect: bool) -> None:
        def callback(x, res):
            self._client.connect_service_finish(res)

        self._client.connect_service(
            self._gdevice.get_object_path(),
            connect,
            None,
            callback,
        )

    def connect_to(self) -> None:
        self.__connect_service(True)

    def disconnect_from(self) -> None:
        self.__connect_service(False)
