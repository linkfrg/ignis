from ._imports import GnomeBluetooth

ADAPTER_STATE = {
    GnomeBluetooth.AdapterState.ABSENT: "absent",
    GnomeBluetooth.AdapterState.ON: "on",
    GnomeBluetooth.AdapterState.TURNING_ON: "turning-on",
    GnomeBluetooth.AdapterState.TURNING_OFF: "turning-off",
    GnomeBluetooth.AdapterState.OFF: "off",
}
