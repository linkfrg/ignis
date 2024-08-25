import os
import sys


__version__ = "0.1dev0"

if "sphinx" not in sys.modules:
    import gi
    from ctypes import CDLL

    CDLL("libgtk4-layer-shell.so")

    gi.require_version("Gtk", "4.0")
    gi.require_version("Gdk", "4.0")
    gi.require_version("Gtk4LayerShell", "1.0")
    gi.require_version("GdkPixbuf", "2.0")

    from gi.repository import GLib
    CACHE_DIR = f"{GLib.get_user_cache_dir()}/ignis/"
    os.makedirs(CACHE_DIR, exist_ok=True)

else:
    CACHE_DIR = None
