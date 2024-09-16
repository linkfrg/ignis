import gi
import sys
from ignis.exceptions import GvcNotFoundError

try:
    if "sphinx" not in sys.modules:
        gi.require_version("Gvc", "1.0")
    from gi.repository import Gvc  # type: ignore
except (ImportError, ValueError):
    raise GvcNotFoundError() from None

__all__ = ["Gvc"]
