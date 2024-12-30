import gi
import sys
from ignis.exceptions import GnomeBluetoothNotFoundError

try:
    if "sphinx" not in sys.modules:
        gi.require_version("GnomeBluetooth", "3.0")
    from gi.repository import GnomeBluetooth  # type: ignore
except (ImportError, ValueError):
    raise GnomeBluetoothNotFoundError() from None

__all__ = ["GnomeBluetooth"]
