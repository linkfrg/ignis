import os
import shutil
from ignis.gobject import IgnisGObject
from ignis.widgets.picture import Picture
from ignis.utils import Utils
from gi.repository import GObject, Gtk, Gdk  # type: ignore
from gi.repository import Gtk4LayerShell as GtkLayerShell
from ignis.exceptions import LayerShellNotSupportedError
from ignis.services import Service
from ignis import CACHE_DIR
from ignis.app import app

CACHE_WALLPAPER_PATH = f"{CACHE_DIR}/wallpaper"


class WallpaperLayerWindow(Gtk.Window):
    def __init__(
        self, wallpaper_path: str, gdkmonitor: Gdk.Monitor, width: int, height: int
    ) -> None:
        if not GtkLayerShell.is_supported():
            raise LayerShellNotSupportedError()

        Gtk.Window.__init__(self, application=app)
        GtkLayerShell.init_for_window(self)

        for anchor in ["LEFT", "RIGHT", "TOP", "BOTTOM"]:
            GtkLayerShell.set_anchor(self, getattr(GtkLayerShell.Edge, anchor), True)

        GtkLayerShell.set_exclusive_zone(self, -1)  # ignore other layers

        GtkLayerShell.set_namespace(
            self, name_space=f"ignis_wallpaper_service_{gdkmonitor.get_model()}"
        )

        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.BACKGROUND)

        GtkLayerShell.set_monitor(self, gdkmonitor)

        self.set_child(
            Picture(
                image=wallpaper_path,
                content_fit="cover",
                width=width,
                height=height,
            )
        )

        self.set_visible(True)


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
        self._windows: list[WallpaperLayerWindow] = []

        self._options = Service.get("options")
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
