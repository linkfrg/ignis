import gi
import os
import sys
import json
import asyncio
import tempfile
from ctypes import CDLL
from gi.events import GLibEventLoopPolicy  # type: ignore
from importlib.metadata import Distribution, PackageNotFoundError
from gi.repository import GLib  # type: ignore


def _get_is_editable_install() -> bool:
    try:
        direct_url = Distribution.from_name("ignis").read_text("direct_url.json")
        if direct_url:
            return json.loads(direct_url).get("dir_info", {}).get("editable", False)

    except PackageNotFoundError:
        pass

    return False


#: The Ignis version.
__version__ = "0.5.dev0"

#: Whether Ignis is imported during the Sphinx documentation build.
is_sphinx_build: bool = "sphinx" in sys.modules

#: Whether Ignis is installed in editable mode.
is_editable_install: bool = _get_is_editable_install()

#: The random temporary directory for this Ignis instance.
TEMP_DIR = tempfile.mkdtemp(prefix="ignis-")

#: The cache directory. Equals ``$XDG_CACHE_HOME/ignis`` by default, or :obj:`TEMP_DIR` during the Sphinx doc build.
CACHE_DIR = f"{GLib.get_user_cache_dir()}/ignis" if not is_sphinx_build else TEMP_DIR

#: Whether libgirepository-2.0 is being used (``True`` for PyGObject 3.51.0 and higher).
#: Always equals ``False`` during the Sphinx doc build.
is_girepository_2_0: bool = (
    gi.version_info >= (3, 51, 0) if not is_sphinx_build else False  # type: ignore
)


def _prepend_to_repo(path: str) -> None:
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


def _init_asyncio() -> None:
    policy = GLibEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)


def _makedirs() -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)


def _load_gtk_layer_shell() -> None:
    try:
        CDLL("libgtk4-layer-shell.so")
    except OSError:
        from ignis.exceptions import Gtk4LayerShellNotFoundError

        raise Gtk4LayerShellNotFoundError() from None


def _require_versions() -> None:
    gi.require_version("Gtk", "4.0")
    gi.require_version("Gdk", "4.0")
    gi.require_version("Gtk4LayerShell", "1.0")
    gi.require_version("GdkPixbuf", "2.0")


def _prepend_gvc() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if not is_editable_install:
        _prepend_to_repo(current_dir)
    else:
        build_libdir = os.path.join(
            os.path.abspath(os.path.join(current_dir, "..")),
            "build",
            f"cp{sys.version_info.major}{sys.version_info.minor}",
            "subprojects",
            "gvc",
        )
        _prepend_to_repo(build_libdir)


def _init() -> None:
    _init_asyncio()
    _makedirs()
    _load_gtk_layer_shell()
    _require_versions()
    _prepend_gvc()


if not is_sphinx_build:
    _init()
