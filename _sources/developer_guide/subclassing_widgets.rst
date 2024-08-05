Subclassing Widgets
=======================

All widgets inherit from the :class:`~ignis.base_widget.BaseWidget` class.

BaseWidget
-----------

.. autoclass:: ignis.base_widget.BaseWidget
    :members:

Widget Class Template
-----------------------

Here is the template for the widget that you want to override.
Replace ``WIDGET_NAME`` with the actual name of the widget.

.. code-block:: python

    from gi.repository import Gtk, GObject
    from ignis.base_widget import BaseWidget


    class WIDGET_NAME(Gtk.WIDGET_NAME, BaseWidget):
        __gtype_name__ = "IgnisWIDGET_NAME"
        __gproperties__ = {**BaseWidget.gproperties}  # this inherits properties from BaseWidget

        def __init__(self, **kwargs):  # accept keyword arguments
            Gtk.Label.__init__(self)
            # if you want to override enums, do it BEFORE BaseWidget.__init__(self, **kwargs)
            # otherwise, the property will be set before it is overridden.
            self.override_enum("SOME_PROPERTY", SOME_ENUM)
            self._custom_property = None  # define protected/private variables for your custom properties BEFORE BaseWidget.__init__(self, **kwargs)
            BaseWidget.__init__(self, **kwargs)  # this sets all properties transferred to kwargs

        @GObject.Property
        def custom_property(self) -> bool:
            return self._custom_property

        @custom_property.setter
        def custom_property(self, value: bool) -> None:
            self._custom_property = value

Docstrings
------------
Use the same patterns as described here: `Documentation <documentation.html>`_.
Additionally, specify the base widget and link to the PyGObject API Reference.
Also, specify whether properties are optional.
It is good practice to include a code example.

.. code-block:: python

    """
    Bases: `Gtk.Label <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Label.html>`_.

    A widget that displays a small amount of text.

    Properties:
        - **justify** (``str``, optional, read-write): description...
        - **ellipsize** (``str``, optional, read-write): description...
        - **wrap_mode** (``str``, optional, read-write): description...

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
