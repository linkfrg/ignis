from collections.abc import Generator
from ._imports import NM


def get_devices(
    client: NM.Client, device_type: NM.DeviceType
) -> Generator[NM.Device, None, None]:
    for d in client.get_devices():
        if d.get_device_type() == device_type:
            yield d

def check_is_vpn(func):
    def wrapper(*args, **kwargs):
        connection = args[2]
        if connection.get_connection_type() == "vpn" or connection.get_connection_type() == "wireguard":
            func(*args, **kwargs)

    return wrapper
