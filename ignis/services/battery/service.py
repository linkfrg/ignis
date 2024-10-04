from ignis.base_service import BaseService
from gi.repository import GObject  # type: ignore
from ignis.dbus import DBusProxy
from ignis.utils import Utils
from .constants import DeviceState


class BatteryService(BaseService):
    def __init__(self) -> None:
        super().__init__()

        self._available: bool = False
        self._percent: int = -1
        self._charging: bool = False
        self._charged: bool = False
        self._icon_name: str = "battery-missing-symbolic"
        self._time_remaining: int = 0
        self._energy: int = 0
        self._energy_full: float = 0.0
        self._energy_rate: float = 0.0

        self._proxy = DBusProxy(
            name="org.freedesktop.UPower",
            object_path="/org/freedesktop/UPower/devices/DisplayDevice",
            interface_name="org.freedesktop.UPower.Device",
            info=Utils.load_interface_xml("org.freedesktop.UPower.Device"),
            bus_type="system",
        )
        self._proxy.proxy.connect("g-properties-changed", self.__sync)
        self.__sync()

    @GObject.Property
    def available(self) -> bool:
        return self._available

    @GObject.Property
    def percent(self) -> int:
        return self._percent

    @GObject.Property
    def charging(self) -> bool:
        return self._charging

    @GObject.Property
    def charged(self) -> bool:
        return self._charged

    @GObject.Property
    def icon_name(self) -> str:
        return self._icon_name

    @GObject.Property
    def time_remaining(self) -> int:
        return self._time_remaining

    @GObject.Property
    def energy(self) -> int:
        return self._energy

    @GObject.Property
    def energy_full(self) -> float:
        return self._energy_full

    @GObject.Property
    def energy_rate(self) -> float:
        return self._energy_rate

    def __sync(self, *args) -> None:
        if not self._proxy.IsPresent:
            self._available = False
            self.notify("available")
            return

        self._charging = self._proxy.State == DeviceState.CHARGING
        self._percent = self._proxy.Percentage
        self._charged = (
            self._proxy.State == DeviceState.FULLY_CHARGED
            or self._proxy.State == DeviceState.CHARGING
            and self._percent == 100
        )

        self._level = self._percent // 10 * 10
        self._state = "-charging" if self._proxy.State == DeviceState.CHARGING else ""
        self._icon_name = (
            "battery-level-100-charged-symbolic"
            if self._charged
            else f"battery-level-{self._level}{self._state}-symbolic"
        )

        self._time_remaining = (
            self._proxy.TimeToFull if self._charging else self._proxy.TimeToEmpty
        )
        self._energy = self._proxy.Energy
        self._energy_full = self._proxy.EnergyFull
        self._energy_rate = self._proxy.EnergyRate

        self.notify_all()
