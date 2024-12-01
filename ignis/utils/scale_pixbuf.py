from typing import Union
from gi.repository import GdkPixbuf  # type: ignore


def scale_pixbuf(
    pixbuf: GdkPixbuf.Pixbuf, width: int, height: int
) -> Union[GdkPixbuf.Pixbuf, None]:
    """
    Scale a ``GdkPixbuf.Pixbuf`` to the given width and height.

    Args:
        pixbuf: The source GdkPixbuf.Pixbuf.
        width: The target width.
        height: The target height.

    Returns:
        The scaled GdkPixbuf.Pixbuf or ``None``.
    """
    return pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
