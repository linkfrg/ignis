import os
from ignis.base_widget import BaseWidget
from gi.repository import Gtk, GObject, GdkPixbuf, Gdk  # type: ignore
from ignis.utils import Utils
from typing import Union


class Icon(Gtk.Image, BaseWidget):
    """
    Bases: :class:`Gtk.Image`

    A widget that displays images or icons in a 1:1 ratio.

    If you want to display an image at its native aspect ratio, see :class:`~ignis.widgets.picture.Picture`.

    .. code-block:: python

        Widget.Icon(
            image='audio-volume-high',
            pixel_size=12
        )

    """

    __gtype_name__ = "IgnisIcon"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, pixel_size: int = -1, **kwargs):
        Gtk.Image.__init__(self)
        self.pixel_size = pixel_size  # this need to set pixel_size BEFORE image
        BaseWidget.__init__(self, **kwargs)

    @GObject.Property
    def image(self) -> Union[str, GdkPixbuf.Pixbuf]:
        """
        - optional, read-write

        The icon name, path to the file, or a ``GdkPixbuf.Pixbuf``.
        """
        return self._image

    @image.setter
    def image(self, value: Union[str, GdkPixbuf.Pixbuf]) -> None:
        self._image = value

        pixbuf = None

        if isinstance(value, GdkPixbuf.Pixbuf):
            pixbuf = value
        elif isinstance(value, str):
            if os.path.isfile(value):
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(value)
            else:
                self.set_from_icon_name(value)
                return

        if pixbuf is None:
            return

        if not self.pixel_size <= 0:
            pixbuf = Utils.scale_pixbuf(pixbuf, self.pixel_size, self.pixel_size)

        paintable = Gdk.Texture.new_for_pixbuf(pixbuf)
        self.set_from_paintable(paintable)
