from collections.abc import Generator
from ._imports import NM


def get_devices(
    client: NM.Client, device_type: NM.DeviceType
) -> Generator[NM.Device, None, None]:
    for d in client.get_devices():
        if d.get_device_type() == device_type:
            yield d
