from gi.repository import GObject  # type: ignore
from ignis.base_service import BaseService
from ._imports import NM
from .wifi import Wifi
from .ethernet import Ethernet
from .vpn import Vpn


class NetworkService(BaseService):
    """
    A Network service. Uses ``NetworkManager``.
    """

    def __init__(self):
        super().__init__()
        self._client = NM.Client.new(None)
        self._wifi = Wifi(self._client)
        self._ethernet = Ethernet(self._client)
        self._vpn = Vpn(self._client)

    @GObject.Property
    def wifi(self) -> Wifi:
        """
        - read-only

        The Wi-Fi object.
        """
        return self._wifi

    @GObject.Property
    def ethernet(self) -> Ethernet:
        """
        - read-only

        The Ethernet object.
        """
        return self._ethernet

    @GObject.Property
    def vpn(self) -> Vpn:
        """
        - read-only

        The Vpn object.
        """
        return self._vpn
