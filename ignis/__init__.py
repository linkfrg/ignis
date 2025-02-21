import gi
import os
import sys
import asyncio
from ctypes import CDLL
from gi.events import GLibEventLoopPolicy  # type: ignore
from gi.repository import GLib  # type: ignore

__version__ = "0.4.dev0"
__lib_dir__ = None
CACHE_DIR = None

if "sphinx" not in sys.modules:
    policy = GLibEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)

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

    current_dir = os.path.dirname(os.path.abspath(__file__))
    build_libdir = os.path.join(
        os.path.abspath(os.path.join(current_dir, "..")),
        "build",
        f"cp{sys.version_info.major}{sys.version_info.minor}",
        "subprojects",
        "gvc",
    )

    for directory in current_dir, build_libdir:
        GIRepository.Repository.prepend_library_path(directory)
        GIRepository.Repository.prepend_search_path(directory)

except TypeError:
    pass
