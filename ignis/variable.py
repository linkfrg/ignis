from .gobject import IgnisGObject
from gi.repository import GObject  # type: ignore
from typing import Any


class Variable(IgnisGObject):
    """
    Bases: :class:`~ignis.gobject.IgnisGObject`

    Simple class that holds a value.

    Example usage:

    .. code-block:: python

        from ignis.variable import Variable

        var = Variable(value=10)
        var.connect("notify::value", lambda x, y: print("Value changed!: ", x.value))

        var.value = 20
    """

    def __init__(self, value: Any = None):
        self._value = value
        super().__init__()

    @GObject.Property
    def value(self) -> Any:
        """
        - optional, read-write

        A value.
        """
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value
