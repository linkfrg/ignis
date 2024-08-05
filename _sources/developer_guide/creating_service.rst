Creating Service
====================

All services should inherits from :class:`~ignis.gobject.IgnisGObject` class.

Here is simple template for service.

.. code-block:: python

    from ignis.gobject import IgnisGObject

    class ExampleService(IgnisGObject):
        __gsignals__ = {
            "some-signal": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
            "arg-signal": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (object,)),
        }

        def __init__(self):
            super().__init__()
            # do other stuff here


Creating D-Bus Service
--------------------------

We will use :class:`~ignis.dbus.DBusService` in this template.
- Use ``PascalCase`` for D-Bus methods and properties naming.
- Also make D-Bus methods/properties private (add ``__`` before name).

.. code-block:: python

    from gi.repository import Gio, GLib
    from ignis.gobject import IgnisGObject
    from ignis.dbus import DBusService

    class ExampleService(IgnisGObject):
        def __init__(self):
            super().__init__()
            self.__dbus = DBusService(...)
            self.__dbus.register_dbus_method("MyMethod", self.__MyMethod)
            self.__dbus.register_dbus_property("MyProperty", self.__MyProperty)

        def __MyMethod(self, invocation: Gio.DBusMethodInvocation, param1: str, param2: int, *args) -> GLib.Variant:
            print("do something")
            return GLib.Variant("(is)", (42, "Hello world!"))

        def __MyProperty(self) -> GLib.Variant:
            return GLib.Variant("(b)", (False,))
