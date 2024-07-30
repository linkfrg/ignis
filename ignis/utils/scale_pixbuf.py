from gi.repository import GdkPixbuf


def scale_pixbuf(pixbuf: GdkPixbuf.Pixbuf, width: int, height: int) -> GdkPixbuf.Pixbuf:
    """
    Scale a ``GdkPixbuf.Pixbuf`` to the given width and height.

    Args:
        pixbuf (``GdkPixbuf.Pixbuf``): The source GdkPixbuf.Pixbuf.
        width (``int``): The target width.
        height (``int``): The target height.
    """
    return pixbuf.scale_simple(
        width, height, GdkPixbuf.InterpType.BILINEAR
    )
