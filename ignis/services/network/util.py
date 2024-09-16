from typing import Iterator
from ._imports import NM


def get_devices(client: NM.Client, device_type: NM.DeviceType) -> Iterator[NM.Device]:
    for d in client.get_devices():
        if d.get_device_type() == device_type:
            yield d
