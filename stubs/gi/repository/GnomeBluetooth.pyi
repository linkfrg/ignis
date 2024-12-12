import enum
from typing import Any, Callable, Sequence

from gi.repository import GObject
from gi.repository import Gio

TYPE_AUDIO: int = 1048800
TYPE_INPUT: int = 13056
_lock = ...  # FIXME Constant
_namespace: str = "GnomeBluetooth"
_version: str = "3.0"

def appearance_to_type(appearance: int) -> Type: ...
def class_to_type(class_: int) -> Type: ...
def send_to_address(address: str, alias: str) -> bool: ...
def type_to_string(type: int) -> str: ...
def uuid_to_string(uuid: str) -> str: ...
def verify_address(bdaddr: str) -> bool: ...

class Client(GObject.Object):
    """
    :Constructors:

    ::

        Client(**properties)
        new() -> GnomeBluetooth.Client

    Object BluetoothClient

    Signals from BluetoothClient:
      device-added (GObject)
      device-removed (gchararray)

    Properties from BluetoothClient:
      num-adapters -> guint: num-adapters
        The number of detected Bluetooth adapters
      default-adapter -> gchararray: default-adapter
        The D-Bus path of the default adapter
      default-adapter-powered -> gboolean: default-adapter-powered
        Whether the default adapter is powered
      default-adapter-state -> BluetoothAdapterState: default-adapter-state
        State of the default adapter
      default-adapter-setup-mode -> gboolean: default-adapter-setup-mode
        Whether the default adapter is visible to others and scanning
      default-adapter-name -> gchararray: default-adapter-name
        The human readable name of the default adapter
      default-adapter-address -> gchararray: default-adapter-address
        The address of the default adapter

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        default_adapter: str
        default_adapter_address: str
        default_adapter_name: str
        default_adapter_powered: bool
        default_adapter_setup_mode: bool
        default_adapter_state: AdapterState
        num_adapters: int

    props: Props = ...
    def __init__(
        self,
        default_adapter_powered: bool = ...,
        default_adapter_setup_mode: bool = ...,
    ): ...
    def connect_service(
        self,
        path: str,
        connect: bool,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def connect_service_finish(self, res: Gio.AsyncResult) -> bool: ...
    def get_devices(self) -> Gio.ListStore: ...
    def has_connected_input_devices(self) -> bool: ...
    @classmethod
    def new(cls) -> Client: ...

class ClientClass(GObject.GPointer):
    """
    :Constructors:

    ::

        ClientClass()
    """

    parent_class: GObject.ObjectClass = ...

class Device(GObject.Object):
    """
    :Constructors:

    ::

        Device(**properties)

    Object BluetoothDevice

    Properties from BluetoothDevice:
      proxy -> GDBusProxy: proxy
        Proxy
      address -> gchararray: address
        Address
      alias -> gchararray: alias
        Alias
      name -> gchararray: name
        Name
      type -> BluetoothType: type
        Type
      icon -> gchararray: icon
        Icon
      paired -> gboolean: paired
        Paired
      trusted -> gboolean: trusted
        Trusted
      connected -> gboolean: connected
        Connected
      legacy-pairing -> gboolean: legacy-pairing
        Legacy Pairing
      uuids -> GStrv: uuids
        UUIDs
      connectable -> gboolean: connectable
        Connectable
      battery-type -> BluetoothBatteryType: battery-type
        Battery Type
      battery-percentage -> gdouble: battery-percentage
        Battery Percentage
      battery-level -> guint: battery-level
        Battery Level

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        address: str
        alias: str
        battery_level: int
        battery_percentage: float
        battery_type: BatteryType
        connectable: bool
        connected: bool
        icon: str
        legacy_pairing: bool
        name: str
        paired: bool
        proxy: Gio.DBusProxy
        trusted: bool
        type: Type
        uuids: list[str]

    props: Props = ...
    def __init__(
        self,
        address: str = ...,
        alias: str = ...,
        battery_level: int = ...,
        battery_percentage: float = ...,
        battery_type: BatteryType = ...,
        connected: bool = ...,
        icon: str = ...,
        legacy_pairing: bool = ...,
        name: str = ...,
        paired: bool = ...,
        proxy: Gio.DBusProxy = ...,
        trusted: bool = ...,
        type: Type = ...,
        uuids: Sequence[str] = ...,
    ): ...
    def dump(self) -> None: ...
    def get_object_path(self) -> str: ...
    def to_string(self) -> str: ...

class DeviceClass(GObject.GPointer):
    """
    :Constructors:

    ::

        DeviceClass()
    """

    parent_class: GObject.ObjectClass = ...

class Type(enum.Enum):
    ANY = 1
    CAMERA = 1024
    COMPUTER = 8
    DISPLAY = 131072
    HEADPHONES = 64
    HEADSET = 32
    JOYPAD = 4096
    KEYBOARD = 256
    MODEM = 4
    MOUSE = 512
    NETWORK = 16
    OTHER_AUDIO = 128
    PHONE = 2
    PRINTER = 2048
    REMOTE_CONTROL = 32768
    SCANNER = 65536
    SPEAKERS = 1048576
    TABLET = 8192
    TOY = 524288
    VIDEO = 16384
    WEARABLE = 262144
    @staticmethod
    def to_string(type: int) -> str: ...

class AdapterState(enum.Enum):
    ABSENT = 0
    OFF = 4
    ON = 1
    TURNING_OFF = 3
    TURNING_ON = 2

class BatteryType(enum.Enum):
    COARSE = 2
    NONE = 0
    PERCENTAGE = 1
