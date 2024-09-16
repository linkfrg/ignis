import os
import shutil
from ignis.utils import Utils
from gi.repository import GObject  # type: ignore
from ignis.services.options import OptionsService
from ignis.base_service import BaseService
from .window import WallpaperLayerWindow
from .constants import CACHE_WALLPAPER_PATH


class WallpaperService(BaseService):
    """
    A simple service to set the wallpaper.
    Supports multiple monitors.

    Properties:
        - **wallpaper** (``str``, read-write): The path to the image.

    **Example usage:**

    .. code-block:: python

        .. code-block:: python

        from ignis.services.wallpaper import WallpaperService

        wallpaper = WallpaperService.get_default()

        wallpaper.set_wallpaper("path/to/image")

    """

    def __init__(self):
        super().__init__()
        self._windows: list[WallpaperLayerWindow] = []

        self._options = OptionsService.get_default()
        self._options.create_option(name="wallpaper", default=None, exists_ok=True)

        self.__sync()

    @GObject.Property
    def wallpaper(self) -> str:
        return self._options.get_option("wallpaper")

    @wallpaper.setter
    def wallpaper(self, value: str) -> None:
        try:
            shutil.copy(value, CACHE_WALLPAPER_PATH)
        except shutil.SameFileError:
            return

        self._options.set_option("wallpaper", value)
        self.__sync()

    def __sync(self) -> None:
        for i in self._windows:
            i.unrealize()

        if not os.path.isfile(CACHE_WALLPAPER_PATH):
            return

        self._windows = []

        for monitor_id in range(Utils.get_n_monitors()):
            gdkmonitor = Utils.get_monitor(monitor_id)
            if not gdkmonitor:
                return

            geometry = gdkmonitor.get_geometry()
            window = WallpaperLayerWindow(
                wallpaper_path=CACHE_WALLPAPER_PATH,
                gdkmonitor=gdkmonitor,
                width=geometry.width,
                height=geometry.height,
            )
            self._windows.append(window)
