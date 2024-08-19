import gi
from ctypes import CDLL
from ignis.__lib_dir__ import LIB_DIR

CDLL("libgtk4-layer-shell.so")

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
gi.require_version("GdkPixbuf", "2.0")
gi.require_version("GIRepository", "2.0")

from gi.repository import GIRepository  # noqa: E402

GIRepository.Repository.prepend_library_path(LIB_DIR)
GIRepository.Repository.prepend_search_path(LIB_DIR)

__version__ = "0.1"
