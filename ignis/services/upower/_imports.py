import gi
import sys
from ignis.exceptions import UPowerNotFoundError

try:
    if "sphinx" not in sys.modules:
        gi.require_version("UPowerGlib", "1.0")
    from gi.repository import UPowerGlib  # type: ignore
except (ImportError, ValueError):
    raise UPowerNotFoundError() from None

__all__ = ["UPowerGlib"]
