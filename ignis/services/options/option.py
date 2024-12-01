from ignis.gobject import IgnisGObject
from gi.repository import GObject  # type: ignore
from typing import Any


class Option(IgnisGObject):
    """
    An option object.
    """

    def __init__(self, name: str, value: Any = None):
        super().__init__()
        self._name = name
        self._value = value

    @GObject.Signal
    def removed(self):
        """
        - Signal

        Emitted when the option is removed.
        """

    @GObject.Property
    def name(self) -> str:
        """
        - read-only

        The name of the option.
        """
        return self._name

    @GObject.Property
    def value(self) -> Any:
        """
        - read-write

        The current value of the option.
        """
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value

    def remove(self) -> None:
        """
        Remove this option.
        """

        self.emit("removed")
