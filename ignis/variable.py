from .gobject import IgnisGObject
from gi.repository import GObject  # type: ignore
from typing import Any

class Variable(IgnisGObject):
    def __init__(self, value: Any = None):
        self._value = value
        super().__init__()

    @GObject.Property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value
