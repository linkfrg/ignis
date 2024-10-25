from __future__ import annotations
from gi.repository import GObject  # type: ignore
from ignis.base_service import BaseService
from ._imports import NM
from .wifi import Wifi
from .ethernet import Ethernet
from .vpn import Vpn


class NetworkService(BaseService):
    """
    A Network service. Uses ``NetworkManager``.

    Properties:
        - **wifi** (:class:`~ignis.services.network.Wifi`, read-only): The Wi-Fi object.
        - **ethernet** (:class:`~ignis.services.network.Ethernet`, read-only): The Ethernet device object.
        - **vpn** (:class:`~ignis.services.network.Vpn`, read-only): The Vpn object.
    """

    def __init__(self):
        super().__init__()
        self._client = NM.Client.new(None)
        self._wifi = Wifi(self._client)
        self._ethernet = Ethernet(self._client)
        self._vpn = Vpn(self._client)

    @GObject.Property
    def wifi(self) -> Wifi:
        return self._wifi

    @GObject.Property
    def ethernet(self) -> Ethernet:
        return self._ethernet

    @GObject.Property
    def vpn(self) -> Vpn:
        return self._vpn
