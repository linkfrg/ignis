import sys

__version__ = "0.1"

if "sphinx" not in sys.modules:
    import gi
    from ctypes import CDLL
    CDLL("libgtk4-layer-shell.so")

    gi.require_version("Gtk", "4.0")
    gi.require_version("Gdk", "4.0")
    gi.require_version("Gtk4LayerShell", "1.0")
    gi.require_version("GdkPixbuf", "2.0")
