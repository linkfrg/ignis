import gi
from ctypes import CDLL

CDLL('libgtk4-layer-shell.so')

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version('Gtk4LayerShell', '1.0')
gi.require_version("GdkPixbuf", "2.0")
gi.require_version("GIRepository", "2.0")

from gi.repository import GIRepository  # noqa: E402
GIRepository.Repository.prepend_library_path('/usr/lib/ignis')
GIRepository.Repository.prepend_search_path('/usr/lib/ignis')
GIRepository.Repository.prepend_library_path('/usr/lib/x86_64-linux-gnu/ignis')
GIRepository.Repository.prepend_search_path('/usr/lib/x86_64-linux-gnu/ignis')

