Widgets
==========

To get widgets, use the universal ``Widget`` class.

.. code-block:: python

   from ignis.widgets import Widget

   Widget.WIDGET_NAME()

Enums
----------------
GTK widgets use enums, which looks similar like this: ``Gtk.Align.START``.
Having to import Gtk and constantly write out the full enum name can be inconvenient.
Therefore, some widgets override their properties to allow using simple Python strings instead of enums.
For example, the ``valign`` property uses the ``Gtk.Align`` enum, 
but you can now pass a string with the actual value of the enum: ``"start"``, ``"center"``, ``"end"``, etc.

.. note::
   Overridden properties do not support enums.
   For example, you cannot pass an enum to the ``valign`` property.

The ``setup`` property
------------------------
You can pass a callback function to the widget costructor as the ``setup`` property.
The widget will be passed to the callback function as an argument.
This can be useful when you need to perform actions when the widget is initialized (for example, connect to signal).

.. code-block:: python

   from ignis.widgets import Widget

   Widget.Label(
      label="you will not see this text", 
      setup=lambda self: self.set_label("instead, you will see this")
   )

Common widget properties
-------------------------

+----------------+---------------+----------------------------------------------------------------------------------------------------------+
| Name           | Type          | Description                                                                                              |
+================+===============+==========================================================================================================+
| css_classes    | ``List[str]`` | List of css classes.                                                                                     |
+----------------+---------------+----------------------------------------------------------------------------------------------------------+
| valign         | ``str``       | Vertical alignment. Possible values: ``"start"``, ``"center"``, ``"end"``, ``"fill"``, ``"baseline"``.   |
+----------------+---------------+----------------------------------------------------------------------------------------------------------+
| halign         | ``str``       | Horizontal alignment. Possible values: ``"start"``, ``"center"``, ``"end"``, ``"fill"``, ``"baseline"``. |
+----------------+---------------+----------------------------------------------------------------------------------------------------------+
| hexpand        | ``bool``      | Whether the widget would like any available extra horizontal space.                                      |
+----------------+---------------+----------------------------------------------------------------------------------------------------------+
| vexpand        | ``bool``      | Whether the widget would like any available extra vertical space.                                        |
+----------------+---------------+----------------------------------------------------------------------------------------------------------+
| tooltip_text   | ``str``       | Tooltip text. Text that will be shown when the user hovers the mouse over the widget.                    |
+----------------+---------------+----------------------------------------------------------------------------------------------------------+
| sensitive      | ``bool``      | Whether the widget responds to input.                                                                    |
+----------------+---------------+----------------------------------------------------------------------------------------------------------+
| visible        | ``bool``      | Whether the widget is visible.                                                                           |
+----------------+---------------+----------------------------------------------------------------------------------------------------------+
| width_request  | ``int``       | Minimum width of the widget.                                                                             |
+----------------+---------------+----------------------------------------------------------------------------------------------------------+
| height_request | ``int``       | Minimum height of the widget.                                                                            |
+----------------+---------------+----------------------------------------------------------------------------------------------------------+
| style          | ``str``       | Inline CSS style that will be applied to this widget.                                                    |
+----------------+---------------+----------------------------------------------------------------------------------------------------------+

Built-in widgets
--------------------

Here is a list of built-in widgets.

.. warning::
   The widget pages only describe the properties that Ignis adds.
   For more information about widget, each page contains a corresponding link to the widget in the PyGObject API reference.

.. hint::
   If the widget you need is not here, you can use it directly from GTK. 
   Please note that it will not support ``style`` property, bindings, and other Ignis features.
   Or, you can manually subclass it, see `Subclassing widgets <developer_guide/subclassing_widgets.rst>`_ for more info.


.. toctree:: 
   :glob:
   :maxdepth: 1

   generated/*