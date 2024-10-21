from ignis.gobject import IgnisGObject
from gi.repository import GObject, GLib  # type: ignore
from ignis.dbus import DBusProxy
from ignis.utils import Utils
from .constants import DEVICE_KIND, DeviceState


class UPowerDevice(IgnisGObject):
    """
    The general class for power devices, including batteries.

    Signals:
        - **removed** (): Emitted when the device has been removed.

    Properties:
        - **object_path** (``str``, read-only): The D-Bus object path of the device.
        - **proxy** (:class:`~ignis.dbus.DBusProxy`, read-only): The instance of :class:`~ignis.dbus.DBusProxy` for this device.
        - **native_path** (``str``, read-only): The native path of the device.
        - **kind** (``str``, read-only): The device kind, e.g. ``"battery"``.
        - **available** (``bool`` read-only): Whether the device is available.
        - **percent** (``float`` read-only): The current percentage of the device.
        - **charging** (``bool`` read-only): Whether the device is currently charging.
        - **charged** (``bool`` read-only): Whether the device is charged.
        - **icon_name** (``str`` read-only): The current icon name.
        - **time_remaining** (``int`` read-only): Time in seconds until fully charged (when charging) or until fully drains (when discharging).
        - **energy** (``float`` read-only): The energy left in the device. Measured in mWh.
        - **energy_full** (``float``, read-only): The amount of energy when the device is fully charged. Measured in mWh.
        - **energy_full_design** (``float``, read-only): The amount of energy when the device was brand new. Measured in mWh.
        - **energy_rate** (``float``, read-only): The rate of discharge or charge. Measured in mW.
        - **charge_cycles** (``int``, read-only): The number of charge cycles for the device, or -1 if unknown or non-applicable.
        - **vendor** (``str``, read-only): The vendor of the device.
        - **model** (``str``, read-only): The model of the device.
        - **serial** (``str``, read-only): The serial number of the device.
        - **power_supply** (``bool``, read-only): Whether the device is powering the system.
        - **technology** (``str``, read-only): The device technology e.g. ``"lithium-ion"``.
        - **temperature** (``float``, read-only): The temperature of the device in degrees Celsius.
        - **voltage** (``float``, read-only): The current voltage of the device.
    """

    __gsignals__ = {
        "removed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, object_path: str):
        super().__init__()

        self.__watching_props: dict[str, tuple[str, ...]] = {}
        self._object_path = object_path

        self._proxy = DBusProxy(
            name="org.freedesktop.UPower",
            object_path=object_path,
            interface_name="org.freedesktop.UPower.Device",
            info=Utils.load_interface_xml("org.freedesktop.UPower.Device"),
            bus_type="system",
        )
        self._proxy.proxy.connect("g-properties-changed", self.__sync)

        self.__watch_property("Percentage", "percent")
        self.__watch_property("Energy", "energy")
        self.__watch_property("EnergyFull", "energy-full")
        self.__watch_property("EnergyRate", "energy-rate")
        self.__watch_property("ChargeCycles", "charge-cycles")
        self.__watch_property("PowerSupply", "power-supply")
        self.__watch_property("Voltage", "voltage")
        self.__watch_property("Temperature", "temperature")
        self.__watch_property("IconName", "icon-name")

        self.__watch_property("IsPresent", "available")
        self.__watch_property("State", "charging", "charged", "time-remaining")
        self.__watch_property("TimeToFull", "time-remaining")
        self.__watch_property("TimeToEmpty", "time-remaining")

    def __watch_property(self, dbus_property: str, *prop_names: str) -> None:
        self.__watching_props[dbus_property] = prop_names

    def __sync(self, proxy, properties: GLib.Variant, invalidated_properties) -> None:
        prop_dict = properties.unpack()

        for dbus_property in prop_dict.keys():
            if dbus_property in self.__watching_props:
                for i in self.__watching_props[dbus_property]:
                    self.notify(i)

    @GObject.Property
    def object_path(self) -> str:
        return self._object_path

    @GObject.Property
    def proxy(self) -> DBusProxy:
        return self._proxy

    @GObject.Property
    def native_path(self) -> str:
        return self._proxy.NativePath

    @GObject.Property
    def kind(self) -> str:
        return DEVICE_KIND.get(self._proxy.Type, "unknown")

    @GObject.Property
    def available(self) -> bool:
        return self._proxy.IsPresent

    @GObject.Property
    def percent(self) -> float:
        return self._proxy.Percentage

    @GObject.Property
    def charging(self) -> bool:
        return self._proxy.State == DeviceState.CHARGING

    @GObject.Property
    def charged(self) -> bool:
        return self._proxy.State == DeviceState.FULLY_CHARGED

    @GObject.Property
    def icon_name(self) -> str:
        return self._proxy.IconName

    @GObject.Property
    def time_remaining(self) -> int:
        return self._proxy.TimeToFull if self.charging else self._proxy.TimeToEmpty

    @GObject.Property
    def energy(self) -> float:
        return self._proxy.Energy

    @GObject.Property
    def energy_full(self) -> float:
        return self._proxy.EnergyFull

    @GObject.Property
    def energy_full_design(self) -> float:
        return self._proxy.EnergyDesign

    @GObject.Property
    def energy_rate(self) -> float:
        return self._proxy.EnergyRate

    @GObject.Property
    def charge_cycles(self) -> int:
        return self._proxy.ChargeCycles

    @GObject.Property
    def vendor(self) -> str:
        return self._proxy.Vendor

    @GObject.Property
    def model(self) -> str:
        return self._proxy.Model

    @GObject.Property
    def serial(self) -> str:
        return self._proxy.Serial

    @GObject.Property
    def power_supply(self) -> bool:
        return self._proxy.PowerSupply

    @GObject.Property
    def technology(self) -> str:
        return DEVICE_KIND.get(self._proxy.Technology, "unknown")

    @GObject.Property
    def temperature(self) -> float:
        return self._proxy.Temperature

    @GObject.Property
    def voltage(self) -> float:
        return self._proxy.Voltage
