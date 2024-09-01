from __future__ import annotations
from gi.repository import GdkPixbuf  # type: ignore


def scale_pixbuf(
    pixbuf: GdkPixbuf.Pixbuf, width: int, height: int
) -> GdkPixbuf.Pixbuf | None:
    """
    Scale a ``GdkPixbuf.Pixbuf`` to the given width and height.

    Args:
        pixbuf (``GdkPixbuf.Pixbuf``): The source GdkPixbuf.Pixbuf.
        width (``int``): The target width.
        height (``int``): The target height.

    Returns:
        ``GdkPixbuf.Pixbuf | None``: The scaled GdkPixbuf.Pixbuf or ``None``.
    """
    return pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
