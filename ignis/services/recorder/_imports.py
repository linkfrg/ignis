import gi
import sys
from ignis.exceptions import GstNotFoundError

try:
    if "sphinx" not in sys.modules:
        gi.require_version("Gst", "1.0")
    from gi.repository import Gst  # type: ignore
except (ImportError, ValueError):
    raise GstNotFoundError(
        "GStreamer not found! To use the recorder service, install GStreamer."
    ) from None

__all__ = ["Gst"]
