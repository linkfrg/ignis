import os
import shutil
from ignis.gobject import IgnisGObject
from ignis.widgets.window import Window
from ignis.widgets.picture import Picture
from ignis.utils import Utils
from gi.repository import GObject
from ignis.services import Service
from ignis import CACHE_DIR

options = Service.get("options")

CACHE_WALLPAPER_PATH = f"{CACHE_DIR}/wallpaper"


class WallpaperService(IgnisGObject):
    """
    A simple service to set the wallpaper.
    Supports multiple monitors.

    Properties:
        - **wallpaper** (``str``, read-write): The path to the image.

    **Example usage:**

    .. code-block:: python

        .. code-block:: python

        from ignis.services import Service

        wallpaper = Service.get("wallpaper")

        wallpaper.set_wallpaper("path/to/image")

    """

    def __init__(self):
        super().__init__()
        self._windows = []
        options.create_option(name="wallpaper", default=None, exists_ok=True)

        self.__sync()

    @GObject.Property
    def wallpaper(self) -> str:
        return options.get_option("wallpaper")

    @wallpaper.setter
    def wallpaper(self, value: str) -> None:
        try:
            shutil.copy(value, CACHE_WALLPAPER_PATH)
        except shutil.SameFileError:
            return

        options.set_option("wallpaper", value)
        self.__sync()

    def __sync(self) -> None:
        for i in self._windows:
            i.unrealize()

        if not os.path.isfile(CACHE_WALLPAPER_PATH):
            return

        self._windows = []

        for monitor_id in range(Utils.get_n_monitors()):
            monitor = Utils.get_monitor(monitor_id)
            geometry = monitor.get_geometry()
            window = Window(
                layer="background",
                exclusivity="ignore",
                monitor=monitor_id,
                namespace=f"ignis_wallpaper_service_{monitor_id}",
                anchor=["left", "right", "top", "bottom"],
                child=Picture(
                    image=CACHE_WALLPAPER_PATH,
                    content_fit="cover",
                    width=geometry.width,
                    height=geometry.height,
                ),
            )
            self._windows.append(window)
