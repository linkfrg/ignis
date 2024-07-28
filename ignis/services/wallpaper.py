import os
import shutil
from ignis.gobject import IgnisGObject
from ignis.widgets.window import Window
from ignis.widgets.picture import Picture
from ignis.utils import Utils
from gi.repository import GLib, GObject
from ignis.services import Service

options = Service.get("options")

options.create_option(name="wallpaper", default=None, exists_ok=True)

CACHE_WALLPAPER_PATH = f"{GLib.get_user_cache_dir()}/ignis/wallpaper"


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

        for i in range(Utils.get_n_monitors()):
            window = Window(
                layer="background",
                exclusivity="ignore",
                monitor=i,
                namespace=f"ignis_wallpaper_service_{i}",
                anchor=["left", "right", "top", "bottom"],
                child=Picture(
                    image=CACHE_WALLPAPER_PATH,
                    content_fit="cover",
                ),
            )
            self._windows.append(window)
