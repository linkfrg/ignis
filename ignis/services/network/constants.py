from ._imports import NM

WIFI_ICON_TEMPLATE = "network-wireless-signal-{}-symbolic"

STATE = {
    NM.DeviceState.UNKNOWN: "unknown",
    NM.DeviceState.UNMANAGED: "unmanaged",
    NM.DeviceState.ACTIVATED: "activated",
    NM.DeviceState.DEACTIVATING: "deactivating",
    NM.DeviceState.FAILED: "failed",
    NM.DeviceState.UNAVAILABLE: "unavailable",
    NM.DeviceState.DISCONNECTED: "disconnected",
    NM.DeviceState.PREPARE: "prepare",
    NM.DeviceState.CONFIG: "config",
    NM.DeviceState.NEED_AUTH: "need_auth",
    NM.DeviceState.IP_CONFIG: "ip_config",
    NM.DeviceState.IP_CHECK: "ip_check",
    NM.DeviceState.SECONDARIES: "secondaries",
}
