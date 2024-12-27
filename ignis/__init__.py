import gi
import os
import sys
from ctypes import CDLL
from gi.repository import GLib  # type: ignore

__version__ = "0.3.dev0"
__lib_dir__ = None
CACHE_DIR = None

if "sphinx" not in sys.modules:
    CACHE_DIR = f"{GLib.get_user_cache_dir()}/ignis"
    os.makedirs(CACHE_DIR, exist_ok=True)

    try:
        CDLL("libgtk4-layer-shell.so")
    except OSError:
        from ignis.exceptions import Gtk4LayerShellNotFoundError

        raise Gtk4LayerShellNotFoundError() from None

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
gi.require_version("GdkPixbuf", "2.0")
gi.require_version("GIRepository", "2.0")

try:
    from gi.repository import GIRepository  # type: ignore

    current_directory = os.path.dirname(os.path.abspath(__file__))

    GIRepository.Repository.prepend_library_path(current_directory)
    GIRepository.Repository.prepend_search_path(current_directory)
except TypeError:
    pass
