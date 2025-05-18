from ignis.base_service import BaseService
from ignis.gobject import IgnisProperty, IgnisSignal
from ignis.app import IgnisApp
from ignis.utils import Utils
from ignis.exceptions import CavaNotFoundError
from .cava import Cava


app = IgnisApp.get_default()


class CavaService(BaseService):
    """
    Service to interact with libcava and provide real-time data.

    Example usage:

    .. code-block:: python

        from ignis.services.cava import CavaService

        cava_service = CavaService.get_default()

        # Get the number of frequency bands
        print(cava_service.bands_count)

        # Get the current frequency bands
        print(cava_service.bands)

        # Start streaming band data
        cava_service.__start_stream()

    Attributes:
        bands_count (int): Number of frequency bands available in libcava.
        bands (list): List of current frequency band values (float).
    """

    def __init__(self):
        super().__init__()

        try:
            self._cava = Cava()
        except Exception as e:
            raise CavaNotFoundError() from e

        self._bands: list[float] = [0.0] * self._cava.bands_count

        if self.is_available:
            self.__start_stream()

    @IgnisProperty
    def is_available(self) -> bool:
        return self._cava is not None

    @IgnisProperty
    def bands_count(self) -> int:
        return self._cava.bands_count

    @IgnisProperty
    def bands(self) -> list[float]:
        return self._bands.copy()

    @IgnisSignal
    def updated(self):
        pass

    def __start_stream(self) -> None:
        Utils.thread(self.__stream_loop)
        app.connect("shutdown", self.stop)

    def __stream_loop(self) -> None:
        self._bands = self._cava.process([0.0] * 512)

        self.notify("bands")
        self.emit("updated")

    def stop(self) -> None:
        if self._cava:
            self._cava.stop()
            self._cava = None
