from gi.repository import Gtk, Pango
from ignis.base_widget import BaseWidget


class Label(Gtk.Label, BaseWidget):
    """
    Bases: `Gtk.Label <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Label.html>`_.

    A widget that displays a small amount of text.

    Properties:
        - **justify** (``str``, optional, read-write): The alignment of the lines in the text of the label relative to each other. This does NOT affect the alignment of the label within its allocation. Possible values: ``"left"``, ``"right"``, ``"center"``, ``"fill"``.
        - **ellipsize** (``str``, optional, read-write): The preferred place to ellipsize the string. Possible values: ``"none"``, ``"start"``, ``"middle"``, ``"end"``.
        - **wrap_mode** (``str``, optional, read-write): If wrap is set, controls how linewrapping is done. Possible values: ``"word"``, ``"char"``, ``"word_char"``.

    .. code-block:: python

        Widget.Label(
            label='heh',
            use_markup=False,
            justify='left',
            wrap=True,
            wrap_mode='word',
            ellipsize='end',
            max_width_chars=52
        )
    """

    __gtype_name__ = "IgnisLabel"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.Label.__init__(self)
        self.override_enum("justify", Gtk.Justification)
        self.override_enum("wrap_mode", Pango.WrapMode)
        self.override_enum("ellipsize", Pango.EllipsizeMode)
        BaseWidget.__init__(self, **kwargs)
