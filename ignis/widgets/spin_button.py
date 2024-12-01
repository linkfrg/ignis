from gi.repository import Gtk, GObject  # type: ignore
from ignis.base_widget import BaseWidget
from typing import Callable


class SpinButton(Gtk.SpinButton, BaseWidget):  # type: ignore
    """
    Bases: :class:`Gtk.SpinButton`

    A widget that allows the user to increment or decrement the displayed value within a specified range.

    .. code-block:: python

        Widget.SpinButton(
            min=0,
            max=100,
            step=1,
            value=50,
            on_change=lambda x, value: print(value)
        )
    """

    __gtype_name__ = "IgnisSpinButton"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, min: int | None = None, max: int | None = None, **kwargs):
        Gtk.SpinButton.__init__(self)
        self._on_change: Callable | None = None
        self.adjustment = Gtk.Adjustment(
            value=0, lower=0, upper=100, step_increment=1, page_increment=0, page_size=0
        )
        self.min = min
        self.max = max
        BaseWidget.__init__(self, **kwargs)

        self.connect("value-changed", self.__invoke_on_change)

    @GObject.Property
    def value(self) -> float:
        """
        - optional, read-write

        The current value.
        """
        return super().get_value()

    @value.setter
    def value(self, value: float) -> None:
        self.adjustment.set_value(value)

    @GObject.Property
    def min(self) -> float:
        """
        - optional, read-write

        Minimum value.
        """
        return self.adjustment.props.lower

    @min.setter
    def min(self, value: float) -> None:
        self.adjustment.props.lower = value

    @GObject.Property
    def max(self) -> float:
        """
        - optional, read-write

        Maximum value.
        """
        return self.adjustment.props.upper

    @max.setter
    def max(self, value: float) -> None:
        self.adjustment.props.upper = value

    @GObject.Property
    def step(self) -> float:
        """
        - optional, read-write

        Step increment.
        """
        return self.adjustment.props.step_increment

    @step.setter
    def step(self, value: float) -> None:
        self.adjustment.props.step_increment = value

    @GObject.Property
    def on_change(self) -> Callable | None:
        """
        - optional, read-write

        The function to call when the value changes.
        """
        return self._on_change

    @on_change.setter
    def on_change(self, value: Callable) -> None:
        self._on_change = value

    def __invoke_on_change(self, *args) -> None:
        if self.on_change:
            self.on_change(self, self.value)
