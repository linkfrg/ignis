import os
import sys

def get_lib_dir() -> str | None:
    try:
        from ignis.__lib_dir__ import __lib_dir__ # type: ignore
        return __lib_dir__
    except ImportError:
        pass

    if sys.base_prefix != sys.prefix:
        return os.path.join(sys.prefix, "lib", "ignis")

    common_lib_dirs = ["/lib/ignis", "/usr/lib/ignis"]
    for lib_dir in common_lib_dirs:
        if os.path.isdir(lib_dir):
            return lib_dir

