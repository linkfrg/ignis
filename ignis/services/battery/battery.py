from ignis.gobject import IgnisGObject
from ._imports import UPowerGlib
from gi.repository import GObject, GLib  # type: ignore
from ignis.dbus import DBusProxy
from ignis.utils import Utils


class Battery(IgnisGObject):
    """
    A battery object.

    Signals:
        - **removed** (:class:`~ignis.services.battery.Battery`): Emitted when the battery has been removed.

    Properties:
        - **device** (``UPowerGlib.Device``, read-only): The instance of ``UPowerGlib.Device``.
        - **native_path** (``str``, read-only): The native path of the device.
        - **available** (``bool`` read-only): Whether the battery is available.
        - **percent** (``float`` read-only): Current percentage.
        - **charging** (``bool`` read-only): Whether the battery is currently charging.
        - **charged** (``bool`` read-only): Whether the battery is charged.
        - **icon_name** (``str`` read-only): The current icon name.
        - **time_remaining** (``int`` read-only): Time in seconds until fully charged (when charging) or until fully drains (when discharging).
        - **energy** (``float`` read-only): The energy left in the device. Measured in mWh.
        - **energy_full** (``float``, read-only): The amount of energy when the device is fully charged. Measured in mWh.
        - **energy_full_design** (``float``, read-only): The amount of energy when the device was brand new. Measured in mWh.
        - **energy_rate** (``float``, read-only): The rate of discharge or charge. Measured in mW.
        - **charge_cycles** (``int``, read-only): The number of charge cycles for the battery, or -1 if unknown or non-applicable.
        - **vendor** (``str``, read-only): The vendor of the device.
        - **model** (``str``, read-only): The model of the device.
        - **serial** (``str``, read-only): The serial number of the device.
        - **power_supply** (``bool``, read-only): Whether the device is powering the system.
        - **technology** (``str``, read-only): The battery technology e.g. ``"lithium-ion"``.
        - **temperature** (``float``, read-only): The temperature of the device in degrees Celsius.
        - **voltage** (``float``, read-only): The current voltage of the device.
    """

    __gsignals__ = {
        "removed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, device: UPowerGlib.Device):
        super().__init__()

        self._device = device

        self._charge_threshold: bool = False
        self._charge_threshold_supported: bool = False
        self._charge_start_threshold: int = 0
        self._charge_end_threshold: int = 0

        self._proxy = DBusProxy(
            name="org.freedesktop.UPower",
            object_path=device.get_object_path(),
            interface_name="org.freedesktop.UPower.Device",
            info=Utils.load_interface_xml("org.freedesktop.UPower.Device"),
            bus_type="system",
        )

        for prop_name in [
            "icon-name",
            "energy",
            "energy-full",
            "energy-rate",
            "charge-cycles",
            "power-supply",
            "voltage",
            "temperature",
        ]:
            self.__conn_dev_notif(prop_name, prop_name)

        self.__conn_dev_notif("is-present", "available")
        self.__conn_dev_notif("percentage", "percent")
        self.__conn_dev_notif("state", "charging", "charged")

        self.__conn_dev_notif("time-to-full", "time-remaining")
        self.__conn_dev_notif("state", "time-remaining")
        self.__conn_dev_notif("time-to-empty", "time-remaining")

        self._proxy.proxy.connect("g-properties-changed", self.__notif_dbus)

    def __conn_dev_notif(self, dev_prop: str, *self_props: str) -> None:
        self._device.connect(
            f"notify::{dev_prop}", lambda x, y: (self.notify(i) for i in self_props)
        )

    def __notif_dbus(
        self, proxy, properties: GLib.Variant, invalidated_properties
    ) -> None:
        prop_dict = properties.unpack()

        if "ChargeThresholdEnabled" in prop_dict:
            self.notify("charge-threshold")
        elif "ChargeThresholdSupported" in prop_dict:
            self.notify("charge-threshold-supported")
        elif "ChargeStartThreshold" in prop_dict:
            self.notify("charge-start-threshold")
        elif "ChargeEndThreshold" in prop_dict:
            self.notify("charge-end-threshold")

    @GObject.Property
    def device(self) -> UPowerGlib.Device:
        return self._device

    @GObject.Property
    def native_path(self) -> str:
        return self._device.props.native_path

    @GObject.Property
    def available(self) -> bool:
        return self._device.props.is_present

    @GObject.Property
    def percent(self) -> float:
        return self._device.props.percentage

    @GObject.Property
    def charging(self) -> bool:
        return self._device.props.state == UPowerGlib.DeviceState.CHARGING

    @GObject.Property
    def charged(self) -> bool:
        return self._device.props.state == UPowerGlib.DeviceState.FULLY_CHARGED

    @GObject.Property
    def icon_name(self) -> str:
        return self._device.props.icon_name

    @GObject.Property
    def time_remaining(self) -> int:
        return (
            self._device.props.time_to_full
            if self.charging
            else self._device.props.time_to_empty
        )

    @GObject.Property
    def energy(self) -> float:
        return self._device.props.energy

    @GObject.Property
    def energy_full(self) -> float:
        return self._device.props.energy_full

    @GObject.Property
    def energy_full_design(self) -> float:
        return self._device.props.energy_full_design

    @GObject.Property
    def energy_rate(self) -> float:
        return self._device.props.energy_rate

    @GObject.Property
    def charge_cycles(self) -> int:
        return self._device.props.charge_cycles

    @GObject.Property
    def vendor(self) -> str:
        return self._device.props.vendor

    @GObject.Property
    def model(self) -> str:
        return self._device.props.model

    @GObject.Property
    def serial(self) -> str:
        return self._device.props.serial

    @GObject.Property
    def power_supply(self) -> bool:
        return self._device.props.power_supply

    @GObject.Property
    def technology(self) -> str:
        return UPowerGlib.Device.technology_to_string(self._device.props.technology)  # type: ignore

    @GObject.Property
    def temperature(self) -> float:
        return self._device.props.temperature

    @GObject.Property
    def voltage(self) -> float:
        return self._device.props.voltage

    @GObject.Property
    def charge_threshold(self) -> bool:
        return self._proxy.ChargeThresholdEnabled

    @charge_threshold.setter
    def charge_threshold(self, value: bool) -> None:
        self._proxy.EnableChargeThreshold("(b)", (value,))

    @GObject.Property
    def charge_threshold_supported(self) -> bool:
        return self._proxy.ChargeThresholdSupported

    @GObject.Property
    def charge_start_threshold(self) -> int:
        return self._proxy.ChargeStartThreshold

    @charge_start_threshold.setter
    def charge_start_threshold(self, value: int) -> None:
        self._proxy.ChargeStartThreshold = GLib.Variant("(u)", (value,))

    @GObject.Property
    def charge_end_threshold(self) -> int:
        return self._proxy.ChargeEndThreshold

    @charge_end_threshold.setter
    def charge_end_threshold(self, value: int) -> None:
        self._proxy.ChargeEndThreshold = GLib.Variant("(u)", (value,))
