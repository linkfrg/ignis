from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisGObject
from ._imports import GnomeBluetooth


class BluetoothDevice(IgnisGObject):
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
