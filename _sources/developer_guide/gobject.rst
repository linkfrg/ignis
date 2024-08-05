Custom GObjects
===============

Adding custom signals
-----------------------

Use the ``__gsignals__`` dictionary to create your custom signals.
To add custom arguments to a signal, add values to the tuple as shown below.

.. code-block:: python

    from ignis.gobject import IgnisGObject

    class ExampleGObject(IgnisGObject):

        __gsignals__ = {
            "my-signal": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
            "arg-signal": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (object,)), # this one will have an extra custom argument
        }

        def __init__(self):
            super().__init__()

To call a signal with custom arguments, use the standart ``.emit()`` method and pass the arguments to it.

.. code-block:: python
    
    some_gobject = ExampleGObject()
    some_gobject.emit("arg-signal", 12)

Adding custom properties
---------------------------

Use the ``@GObject.Property`` decorator to add a custom property.
The syntax is similar to the built-in Python decorator ``@property``.

.. code-block:: python

    from ignis.gobject import IgnisGObject

    class ExampleGObject(IgnisGObject):
        def __init__(self):
            super().__init__()
            self._custom_property = False

        @GObject.Property  # use this decorator to create GObject properties
        def custom_property(self) -> bool:  # bool here is for example
            return self._custom_property

        @custom_property.setter  # use this if you want to make the property read-write. Otherwise, the property will be read-only.
        def custom_property(self, value: bool) -> None:
            self._custom_property = value