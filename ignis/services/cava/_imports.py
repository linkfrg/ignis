from ignis.exceptions import CffiNotFoundError
from ignis import is_sphinx_build

try:
    if not is_sphinx_build:
        from cffi import FFI  # type: ignore
except (ImportError, ValueError):
    raise CffiNotFoundError() from None

__all__ = ["FFI"]
