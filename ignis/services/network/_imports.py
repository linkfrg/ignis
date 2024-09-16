import gi
import sys
from ignis.exceptions import NetworkManagerNotFoundError

try:
    if "sphinx" not in sys.modules:
        gi.require_version("NM", "1.0")
    from gi.repository import NM  # type: ignore
except (ImportError, ValueError):
    raise NetworkManagerNotFoundError() from None

__all__ = ["NM"]
