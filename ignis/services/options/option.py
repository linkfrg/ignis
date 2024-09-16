from ignis.gobject import IgnisGObject
from gi.repository import GObject  # type: ignore
from typing import Any


class Option(IgnisGObject):
    """
    :meta private:
    """

    def __init__(self, name: str, value: Any = None):
        super().__init__()
        self._name = name
        self._value = value

    @GObject.Property
    def name(self) -> str:
        return self._name

    @GObject.Property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value
