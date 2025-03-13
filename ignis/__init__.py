import gi
import os
import sys
import json
import asyncio
from ctypes import CDLL
from gi.events import GLibEventLoopPolicy  # type: ignore
from importlib.metadata import Distribution, PackageNotFoundError
from gi.repository import GLib  # type: ignore

__version__ = "0.4.dev0"
__lib_dir__ = None
CACHE_DIR = None

is_sphinx_build: bool = "sphinx" in sys.modules
is_editable_install: bool = False

try:
    direct_url = Distribution.from_name("ignis").read_text("direct_url.json")
    if direct_url:
        is_editable_install = (
            json.loads(direct_url).get("dir_info", {}).get("editable", False)
        )

except PackageNotFoundError:
    pass

if not is_sphinx_build:
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

from gi.repository import GIRepository  # type: ignore  # noqa: E402


def prepend_to_repo(path: str) -> None:
    try:
        GIRepository.Repository.prepend_library_path(path)
        GIRepository.Repository.prepend_search_path(path)
    except TypeError:
        pass


current_dir = os.path.dirname(os.path.abspath(__file__))

if not is_editable_install:
    prepend_to_repo(current_dir)
else:
    build_libdir = os.path.join(
        os.path.abspath(os.path.join(current_dir, "..")),
        "build",
        f"cp{sys.version_info.major}{sys.version_info.minor}",
        "subprojects",
        "gvc",
    )
    prepend_to_repo(build_libdir)
