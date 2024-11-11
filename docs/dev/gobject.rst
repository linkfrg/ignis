GObject
============

All GObjects in Ignis should inherit from the :class:`~ignis.gobject.IgnisGObject` class,
which provides additional functionality and thread-safe signal operations.

All other stuff (properties, signals) follow the standard PyGObject way.
Use ``@GObject.Property`` and ``@GObject.Signal``  decorators to define properties and signals respectively.