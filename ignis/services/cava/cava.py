from ._imports import FFI
from .constants import CAVA_CDEF
from ignis.gobject import IgnisGObject, IgnisProperty

ffi = FFI()

ffi.cdef(CAVA_CDEF)


class Cava(IgnisGObject):
    """
    Wrapper for libcava.
    """

    def __init__(
        self,
        bands: int = 32,
        sample_rate: int = 44100,
        stereo: int = 1,
        framerate: int = 1,
        gravity: float = 0.77,
        integral: int = 50,
        monstercat: int = 10000,
    ):
        try:
            self._ffi = ffi
            self._lib = self._ffi.dlopen("libcava.so")
            self._bands = bands

            self._plan = self._lib.cava_init(
                bands, sample_rate, stereo, framerate, gravity, integral, monstercat
            )

            self._input_buffer = self._ffi.new("double[512]")
            self._output_buffer = self._ffi.new(f"double[{bands}]")

        except Exception:
            self._ffi = None
            self._lib = None
            self._plan = None
            self._bands = 0

    @IgnisProperty
    def bands_count(self) -> int:
        """
        Number of frequency bands.
        """
        return self._bands

    def process(self, input_data: list[float]) -> list[float]:
        """Process audio input and return frequency bands.

        Args:
            input_data: List of float values representing audio samples.
        """
        if self._lib is None or self._plan is None:
            return [0.0] * self._bands

        try:
            for i in range(min(len(input_data), 512)):
                self._input_buffer[i] = input_data[i]

            self._lib.cava_execute(
                self._input_buffer, 512, self._output_buffer, self._plan
            )

            output_bands = [self._output_buffer[i] for i in range(self._bands)]
            return output_bands

        except Exception:
            return [0.0] * self._bands

    def stop(self) -> None:
        """
        Free resources associated with Cava.
        """
        if self._lib is None or self._plan is None:
            return

        self._lib.cava_destroy(self._plan)
        self._plan = None
