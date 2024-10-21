import enum

DEVICE_KIND = {
    None: "unknown",
    0: "unknown",
    1: "line-power",
    2: "battery",
    3: "ups",
    4: "monitor",
    5: "mouse",
    6: "keyboard",
    7: "pda",
    8: "phone",
    9: "media-player",
    10: "tablet",
    11: "computer",
    12: "gaming-input",
    13: "pen",
    14: "touchpad",
    15: "modem",
    16: "network",
    17: "headset",
    18: "speakers",
    19: "headphones",
    20: "video",
    21: "other-audio",
    22: "remote-control",
    23: "printer",
    24: "scanner",
    25: "camera",
    26: "wearable",
    27: "toy",
    28: "bluetooth-generic",
}

TECHNOLOGY = {
    0: "unknown",
    1: "lithium-ion",
    2: "lithium-polymer",
    3: "lithium-iron-phosphate",
    4: "lead-acid",
    5: "nickel-cadmium",
    6: "nickel-metal-hydride",
}


class DeviceState(enum.Enum):
    UNKNOWN = 0
    CHARGING = 1
    DISCHARGING = 2
    EMPTY = 3
    FULLY_CHARGED = 4
    PENDING_CHARGE = 5
    PENDING_DISCHARGE = 6
