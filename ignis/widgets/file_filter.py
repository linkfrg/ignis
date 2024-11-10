from gi.repository import Gtk, GObject  # type: ignore
from ignis.gobject import IgnisGObject


class FileFilter(Gtk.FileFilter, IgnisGObject):
    """
    Bases: :class:`Gtk.FileFilter`

    .. note::
        This is not a regular widget.
        It doesn't support common widget properties and cannot be added as a child to a container.

    A file filter.
    Intended for use in :class:`~ignis.widgets.Widget.FileDialog`.
    Uses MIME types, `here <https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types>`_ is a list of common MIME types.

    .. code-block :: python

        Widget.FileFilter(
            mime_types=["image/jpeg", "image/png"],
            default=True,
            name="Images JPEG/PNG",
        )
    """

    __gtype_name__ = "IgnisFileFilter"

    def __init__(self, mime_types: list[str], **kwargs):
        Gtk.FileFilter.__init__(self)
        self._default: bool = False
        self._mime_types = mime_types
        IgnisGObject.__init__(self, **kwargs)

        for i in mime_types:
            self.add_mime_type(i)

    @GObject.Property
    def mime_types(self) -> list[str]:
        """
        - required, read-only

        A list of MIME types.
        """
        return self._mime_types

    @GObject.Property
    def default(self) -> bool:
        """
        - optional, read-write

        Whether the filter will be selected by default.
        """
        return self._default

    @default.setter
    def default(self, value: bool) -> None:
        self._default = value
