import gi
from ignis.exceptions import GstNotFoundError
from ignis import is_sphinx_build

try:
    if not is_sphinx_build:
        gi.require_version("Gst", "1.0")
    from gi.repository import Gst  # type: ignore
except (ImportError, ValueError):
    raise GstNotFoundError(
        "GStreamer not found! To use the recorder service, install GStreamer."
    ) from None

__all__ = ["Gst"]
