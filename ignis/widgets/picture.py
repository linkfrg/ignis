import os
from ignis.base_widget import BaseWidget
from gi.repository import Gtk, GObject, GdkPixbuf, Gdk
from typing import Union
from ignis.utils import Utils


class Picture(Gtk.Picture, BaseWidget):
    """
    Bases: `Gtk.Picture <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Picture.html>`_.

    A widget that displays an image at its native aspect ratio.

    Properties:
        - **image** (``Union[str, GdkPixbuf.Pixbuf]``, optional, read-write): Icon name, path to an image or ``GdkPixbuf.Pixbuf``.
        - **width** (``int``, optional, read-write): Width of the image.
        - **height** (``int``, optional, read-write): Height of the image.
        - **content_fit** (``str``, optional, read-write): Controls how a content should be made to fit inside an allocation. Possible values: ``"fill"``, ``"contain"``, ``"cover"``, ``"scale_down"``.

    **Content fit:**
        - **"fill"**: Make the content fill the entire allocation, without taking its aspect ratio in consideration.
        - **"contain"**: Scale the content to fit the allocation, while taking its aspect ratio in consideration..
        - **"cover"**: Cover the entire allocation, while taking the content aspect ratio in consideration.
        - **"scale_down"**: The content is scaled down to fit the allocation, if needed, otherwise its original size is used.

        For more info, see `Gtk.ContentFit <https://lazka.github.io/pgi-docs/Gtk-4.0/enums.html#Gtk.ContentFit>`_

    .. code-block:: python

        Widget.Picture(
            image='path/to/img',
            width=20,
            height=30
        )
    """

    __gtype_name__ = "IgnisPicture"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self, content_fit: str = "contain", width: int = -1, height: int = -1, **kwargs
    ):
        Gtk.Picture.__init__(self)
        self.override_enum("content_fit", Gtk.ContentFit)

        # avoid custom setters to avoid running the __draw function multiple times during initialization
        self._image = None
        self._width = width
        self._height = height
        self.width_request = width
        self.height_request = height

        self.content_fit = content_fit

        BaseWidget.__init__(self, **kwargs)

    @GObject.Property
    def image(self) -> Union[str, GdkPixbuf.Pixbuf]:
        return self._image

    @image.setter
    def image(self, value: Union[str, GdkPixbuf.Pixbuf]) -> None:
        self._image = value
        self.__draw(value)

    @GObject.Property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value
        self.width_request = value
        self.__draw(self.image)

    @GObject.Property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value
        self.height_request = value
        self.__draw(self.image)

    def __draw(self, image: Union[str, GdkPixbuf.Pixbuf]):
        if isinstance(image, GdkPixbuf.Pixbuf):
            self.__set_from_pixbuf(image)
        elif isinstance(image, str):
            if os.path.isfile(image):
                if os.path.splitext(image)[1] == ".svg":
                    self.__set_from_svg(image)
                else:
                    self.__set_from_file(image)
            else:
                self.__set_from_icon_name(image)

    def __set_from_pixbuf(self, pixbuf: GdkPixbuf.Pixbuf) -> None:
        scalled_pixbuf = self.__scale_pixbuf(pixbuf, self.width, self.height)

        paintable = Gdk.Texture.new_for_pixbuf(scalled_pixbuf)
        self.set_paintable(paintable)

    def __set_from_file(self, filename: str) -> None:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
        self.__set_from_pixbuf(pixbuf)

    def __set_from_svg(self, filename: str) -> None:
        if not filename:
            return
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename, self.width, self.height, True
        )
        paintable = Gdk.Texture.new_for_pixbuf(pixbuf)
        self.set_paintable(paintable)
        return

    def __set_from_icon_name(self, icon_name: str) -> None:
        size = max(self.height, self.width)
        if size <= 0:
            size = 16

        paintable = Utils.get_paintable(self, icon_name, size)
        self.set_paintable(paintable)
        self.__set_from_svg(paintable.get_file().get_path())

    def __scale_pixbuf(
        self, pixbuf: GdkPixbuf.Pixbuf, width: int, height: int
    ) -> GdkPixbuf.Pixbuf:
        if width <= 0:
            return pixbuf

        if height <= 0:
            return pixbuf

        if self.content_fit == "cover":
            pixbuf = Utils.crop_pixbuf(pixbuf, width, height)

        return Utils.scale_pixbuf(pixbuf, width, height)
