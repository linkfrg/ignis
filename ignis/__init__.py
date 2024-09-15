import gi
import os
import sys
from ctypes import CDLL
from gi.repository import GLib  # type: ignore
from ignis.exceptions import Gtk4LayerShellNotFoundError

__version__ = "0.1dev0"
CACHE_DIR = f"{GLib.get_user_cache_dir()}/ignis"

if "sphinx" not in sys.modules:
    os.makedirs(CACHE_DIR, exist_ok=True)

    try:
        CDLL("libgtk4-layer-shell.so")
    except OSError:
        raise Gtk4LayerShellNotFoundError() from None

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
gi.require_version("GdkPixbuf", "2.0")
