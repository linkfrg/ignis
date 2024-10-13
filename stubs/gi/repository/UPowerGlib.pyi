import enum
from typing import Any, Callable
from gi.repository import GObject
from gi.repository import Gio


MAJOR_VERSION: int = 1
MICRO_VERSION: int = 6
MINOR_VERSION: int = 90
_lock = ... # FIXME Constant
_namespace: str = "UPowerGlib"
_version: str = "1.0"

class Client(GObject.Object, Gio.AsyncInitable, Gio.Initable):  # type: ignore
    """
    :Constructors:

    ::

        Client(**properties)
        new() -> UPowerGlib.Client
        new_finish(res:Gio.AsyncResult) -> UPowerGlib.Client
        new_full(cancellable:Gio.Cancellable=None) -> UPowerGlib.Client

    Object UpClient

    Signals from UpClient:
      device-added (UpDevice)
      device-removed (gchararray)

    Properties from UpClient:
      daemon-version -> gchararray: Daemon version
      on-battery -> gboolean: If the computer is on battery power
      lid-is-closed -> gboolean: If the laptop lid is closed
      lid-is-present -> gboolean: If a laptop lid is present

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        daemon_version: str
        lid_is_closed: bool
        lid_is_present: bool
        on_battery: bool
    props: Props = ...  # type: ignore
    parent: GObject.Object = ...
    priv: ClientPrivate = ...
    def do_device_added(self, device: Device) -> None: ...
    def do_device_removed(self, object_path: str) -> None: ...
    def get_critical_action(self) -> str: ...
    def get_daemon_version(self) -> str: ...
    def get_devices(self) -> list[Device]: ...
    def get_devices2(self) -> list[Device]: ...
    def get_devices_async(self, cancellable: Gio.Cancellable | None = None, callback: Callable[..., None] | None = None, *user_data: Any) -> None: ...
    def get_devices_finish(self, res: Gio.AsyncResult) -> list[Device]: ...
    def get_display_device(self) -> Device: ...
    def get_lid_is_closed(self) -> bool: ...
    def get_lid_is_present(self) -> bool: ...
    def get_on_battery(self) -> bool: ...
    @classmethod
    def new(cls) -> Client: ...
    @staticmethod
    def new_async(cancellable: Gio.Cancellable | None = None, callback: Callable[..., None] | None = None, *user_data: Any) -> None: ...
    @classmethod
    def new_finish(cls, res: Gio.AsyncResult) -> Client: ...
    @classmethod
    def new_full(cls, cancellable: Gio.Cancellable | None = None) -> Client: ...


class ClientClass(GObject.GPointer):
    """
    :Constructors:

    ::

        ClientClass()
    """
    parent_class: GObject.ObjectClass = ...
    device_added: Callable[[Client, Device], None] = ...
    device_removed: Callable[[Client, str], None] = ...
    _up_client_reserved1: None = ...
    _up_client_reserved2: None = ...
    _up_client_reserved3: None = ...
    _up_client_reserved4: None = ...
    _up_client_reserved5: None = ...
    _up_client_reserved6: None = ...
    _up_client_reserved7: None = ...
    _up_client_reserved8: None = ...

class ClientPrivate(GObject.GPointer): ...

class Device(GObject.Object):
    """
    :Constructors:

    ::

        Device(**properties)
        new() -> UPowerGlib.Device

    Object UpDevice

    Properties from UpDevice:
      update-time -> guint64: update-time
      vendor -> gchararray: vendor
      model -> gchararray: model
      serial -> gchararray: serial
      native-path -> gchararray: native-path
      power-supply -> gboolean: power-supply
      online -> gboolean: online
      is-present -> gboolean: is-present
      is-rechargeable -> gboolean: is-rechargeable
      has-history -> gboolean: has-history
      has-statistics -> gboolean: has-statistics
      kind -> guint: kind
      state -> guint: state
      technology -> guint: technology
      capacity -> gdouble: capacity
      energy -> gdouble: energy
      energy-empty -> gdouble: energy-empty
      energy-full -> gdouble: energy-full
      energy-full-design -> gdouble: energy-full-design
      energy-rate -> gdouble: energy-rate
      voltage -> gdouble: voltage
      luminosity -> gdouble: luminosity
      time-to-empty -> gint64: time-to-empty
      time-to-full -> gint64: time-to-full
      percentage -> gdouble: percentage
      temperature -> gdouble: temperature
      warning-level -> guint: warning-level
      battery-level -> guint: battery-level
      icon-name -> gchararray: icon-name
      charge-cycles -> gint: charge-cycles
      charge-start-threshold -> guint: charge-start-threshold
      charge-end-threshold -> guint: charge-end-threshold
      charge-threshold-enabled -> gboolean: charge-threshold-enabled
      charge-threshold-supported -> gboolean: charge-threshold-supported

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        battery_level: int
        capacity: float
        charge_cycles: int
        charge_end_threshold: int
        charge_start_threshold: int
        charge_threshold_enabled: bool
        charge_threshold_supported: bool
        energy: float
        energy_empty: float
        energy_full: float
        energy_full_design: float
        energy_rate: float
        has_history: bool
        has_statistics: bool
        icon_name: str
        is_present: bool
        is_rechargeable: bool
        kind: int
        luminosity: float
        model: str
        native_path: str
        online: bool
        percentage: float
        power_supply: bool
        serial: str
        state: int
        technology: int
        temperature: float
        time_to_empty: int
        time_to_full: int
        update_time: int
        vendor: str
        voltage: float
        warning_level: int
    props: Props = ...  # type: ignore
    parent: GObject.Object = ...
    priv: DevicePrivate = ...
    def __init__(self, battery_level: int = ...,
                 capacity: float = ...,
                 charge_cycles: int = ...,
                 charge_end_threshold: int = ...,
                 charge_start_threshold: int = ...,
                 charge_threshold_enabled: bool = ...,
                 charge_threshold_supported: bool = ...,
                 energy: float = ...,
                 energy_empty: float = ...,
                 energy_full: float = ...,
                 energy_full_design: float = ...,
                 energy_rate: float = ...,
                 has_history: bool = ...,
                 has_statistics: bool = ...,
                 icon_name: str = ...,
                 is_present: bool = ...,
                 is_rechargeable: bool = ...,
                 kind: int = ...,
                 luminosity: float = ...,
                 model: str = ...,
                 native_path: str = ...,
                 online: bool = ...,
                 percentage: float = ...,
                 power_supply: bool = ...,
                 serial: str = ...,
                 state: int = ...,
                 technology: int = ...,
                 temperature: float = ...,
                 time_to_empty: int = ...,
                 time_to_full: int = ...,
                 update_time: int = ...,
                 vendor: str = ...,
                 voltage: float = ...,
                 warning_level: int = ...): ...
    def get_history_sync(self, type: str, timespec: int, resolution: int, cancellable: Gio.Cancellable | None = None) -> list[HistoryItem]: ...
    def get_object_path(self) -> str: ...
    def get_statistics_sync(self, type: str, cancellable: Gio.Cancellable | None = None) -> list[StatsItem]: ...
    @staticmethod
    def kind_from_string(type: str) -> DeviceKind: ...
    @staticmethod
    def kind_to_string(type_enum: DeviceKind) -> str: ...
    @staticmethod
    def level_from_string(level: str) -> DeviceLevel: ...
    @staticmethod
    def level_to_string(level_enum: DeviceLevel) -> str: ...
    @classmethod
    def new(cls) -> Device: ...
    def refresh_sync(self, cancellable: Gio.Cancellable | None = None) -> bool: ...
    def set_object_path_sync(self, object_path: str, cancellable: Gio.Cancellable | None = None) -> bool: ...
    @staticmethod
    def state_from_string(state: str) -> DeviceState: ...
    @staticmethod
    def state_to_string(state_enum: DeviceState) -> str: ...
    @staticmethod
    def technology_from_string(technology: str) -> DeviceTechnology: ...
    @staticmethod
    def technology_to_string(technology_enum: DeviceTechnology) -> str: ...
    def to_text(self) -> str: ...


class DeviceClass(GObject.GPointer):
    """
    :Constructors:

    ::

        DeviceClass()
    """
    parent_class: GObject.ObjectClass = ...
    _up_device_reserved1: None = ...
    _up_device_reserved2: None = ...
    _up_device_reserved3: None = ...
    _up_device_reserved4: None = ...
    _up_device_reserved5: None = ...
    _up_device_reserved6: None = ...
    _up_device_reserved7: None = ...
    _up_device_reserved8: None = ...

class DevicePrivate(GObject.GPointer): ...

class HistoryItem(GObject.Object):
    """
    :Constructors:

    ::

        HistoryItem(**properties)
        new() -> UPowerGlib.HistoryItem

    Object UpHistoryItem

    Properties from UpHistoryItem:
      value -> gdouble: value
      time -> guint: time
      state -> guint: state

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        state: int
        time: int
        value: float
    props: Props = ...  # type: ignore
    parent: GObject.Object = ...
    priv: HistoryItemPrivate = ...
    def __init__(self, state: int = ...,
                 time: int = ...,
                 value: float = ...): ...
    def get_state(self) -> DeviceState: ...
    def get_time(self) -> int: ...
    def get_value(self) -> float: ...
    @classmethod
    def new(cls) -> HistoryItem: ...
    def set_from_string(self, text: str) -> bool: ...
    def set_state(self, state: DeviceState) -> None: ...
    def set_time(self, time: int) -> None: ...
    def set_time_to_present(self) -> None: ...
    def set_value(self, value: float) -> None: ...
    def to_string(self) -> str: ...


class HistoryItemClass(GObject.GPointer):
    """
    :Constructors:

    ::

        HistoryItemClass()
    """
    parent_class: GObject.ObjectClass = ...

class HistoryItemPrivate(GObject.GPointer): ...

class StatsItem(GObject.Object):
    """
    :Constructors:

    ::

        StatsItem(**properties)
        new() -> UPowerGlib.StatsItem

    Object UpStatsItem

    Properties from UpStatsItem:
      value -> gdouble: value
      accuracy -> gdouble: accuracy

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        accuracy: float
        value: float
    props: Props = ...  # type: ignore
    parent: GObject.Object = ...
    priv: StatsItemPrivate = ...
    def __init__(self, accuracy: float = ...,
                 value: float = ...): ...
    def get_accuracy(self) -> float: ...
    def get_value(self) -> float: ...
    @classmethod
    def new(cls) -> StatsItem: ...
    def set_accuracy(self, accuracy: float) -> None: ...
    def set_value(self, value: float) -> None: ...


class StatsItemClass(GObject.GPointer):
    """
    :Constructors:

    ::

        StatsItemClass()
    """
    parent_class: GObject.ObjectClass = ...

class StatsItemPrivate(GObject.GPointer): ...

class DeviceKind(enum.Enum):
    BATTERY = 2
    BLUETOOTH_GENERIC = 28
    CAMERA = 25
    COMPUTER = 11
    GAMING_INPUT = 12
    HEADPHONES = 19
    HEADSET = 17
    KEYBOARD = 6
    LAST = 29
    LINE_POWER = 1
    MEDIA_PLAYER = 9
    MODEM = 15
    MONITOR = 4
    MOUSE = 5
    NETWORK = 16
    OTHER_AUDIO = 21
    PDA = 7
    PEN = 13
    PHONE = 8
    PRINTER = 23
    REMOTE_CONTROL = 22
    SCANNER = 24
    SPEAKERS = 18
    TABLET = 10
    TOUCHPAD = 14
    TOY = 27
    UNKNOWN = 0
    UPS = 3
    VIDEO = 20
    WEARABLE = 26

class DeviceLevel(enum.Enum):
    ACTION = 5
    CRITICAL = 4
    DISCHARGING = 2
    FULL = 8
    HIGH = 7
    LAST = 9
    LOW = 3
    NONE = 1
    NORMAL = 6
    UNKNOWN = 0

class DeviceState(enum.Enum):
    CHARGING = 1
    DISCHARGING = 2
    EMPTY = 3
    FULLY_CHARGED = 4
    LAST = 7
    PENDING_CHARGE = 5
    PENDING_DISCHARGE = 6
    UNKNOWN = 0

class DeviceTechnology(enum.Enum):
    LAST = 7
    LEAD_ACID = 4
    LITHIUM_ION = 1
    LITHIUM_IRON_PHOSPHATE = 3
    LITHIUM_POLYMER = 2
    NICKEL_CADMIUM = 5
    NICKEL_METAL_HYDRIDE = 6
    UNKNOWN = 0


