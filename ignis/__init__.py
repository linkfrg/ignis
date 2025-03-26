import gi
import os
import sys
import json
import asyncio
from ctypes import CDLL
from gi.events import GLibEventLoopPolicy  # type: ignore
from importlib.metadata import Distribution, PackageNotFoundError
from gi.repository import GLib  # type: ignore

__version__ = "0.5.dev0"
__lib_dir__ = None
CACHE_DIR = None

is_sphinx_build: bool = "sphinx" in sys.modules
is_editable_install: bool = False
is_girepository_2_0: bool

if not is_sphinx_build:
    is_girepository_2_0 = gi.version_info >= (3, 51, 0)  # type: ignore
else:
    is_girepository_2_0 = False

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


def prepend_to_repo(path: str) -> None:
    if is_girepository_2_0:
        # Hacky? yes
        # But getting GIRepository from gi.repository and using its prepend methods results in no effect
        # So, we import Repository from _gi, which is used by the gi module itself (you can see that in gi/__init__.py)
        from gi._gi import Repository  # type: ignore # noqa: E402

        # Original GIRepository.Repository 3.0 doesn't have get_default()
        # But! This Repository magically have it, idk why
        # And you must call it, otherwise (using prepend methods as class methods) an error will be thrown
        # See how gi.require_version() works internally
        repo = Repository.get_default()
    else:
        gi.require_version("GIRepository", "2.0")
        from gi.repository import GIRepository  # type: ignore

        repo = GIRepository.Repository

    repo.prepend_library_path(path)
    repo.prepend_search_path(path)


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
