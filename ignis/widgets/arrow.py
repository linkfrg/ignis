from gi.repository import GObject  # type: ignore
from ignis.widgets.icon import Icon
from ignis.utils import Utils

DIRECTION = {
    "right": "pan-end-symbolic",
    "left": "pan-start-symbolic",
    "up": "pan-up-symbolic",
    "down": "pan-down-symbolic",
}


class Arrow(Icon):
    """
    Bases: :class:`~ignis.widgets.icon.Icon`

    An arrow icon that can rotate (with animation!).
    Useful for dropdown lists.

    .. hint::
        If you are looking for a button with an arrow that rotates on click,
        see :class:`~ignis.widgets.Widget.ArrowButton`.

    .. hint::
        You can set your custom icon name or image using the ``image`` property.

    .. code-block:: python

        Widget.Arrow(
            pixel_size=20, # inherited from Widget.Icon
            rotated=False,
            degree=90,
            time=135,
            direction="right",
            counterclockwise=False,
            # image="some-icon/OR/path/to/file" # if you want a custom icon name or image
        )
    """

    __gtype_name__ = "IgnisArrow"

    def __init__(self, **kwargs):
        self._rotated: bool = False
        self.__deg: int = 0  # Current rotation degree
        self.__step: int = 0  # How many steps to do
        self._degree: int = 90  # Target rotation degree
        self._time: int = 135  # Rotation time in milliseconds
        self._direction: str = "right"
        self._counterclockwise: bool = False

        self.__update_step()

        super().__init__(**kwargs)

        if all(key not in kwargs for key in ["direction", "image", "icon_name"]):
            self.direction = self._direction

    def __rotate(self, value: bool) -> None:
        if value:
            if not self.counterclockwise:
                self.__deg += self.__step
            else:
                self.__deg -= self.__step
        else:
            if self.__deg == 0:
                return

            if not self.counterclockwise:
                self.__deg -= self.__step
            else:
                self.__deg += self.__step

        self.style = f"-gtk-icon-transform: rotate({self.__deg}deg);"

    @GObject.Property
    def rotated(self) -> bool:
        """
        - optional, read-write

        Whether the arrow is rotated.

        Default: ``False``.
        """
        return self._rotated

    @rotated.setter
    def rotated(self, value: bool) -> None:
        steps = self.degree // self.__step
        interval = self.time // steps

        for i in range(steps):
            Utils.Timeout(interval * i, self.__rotate, value)

        self._rotated = value

    def __update_step(self) -> None:
        min_steps = 9  # Minimum steps for smooth animation
        steps = max(
            self.time // 15, min_steps
        )  # Calculate steps based on time, with a minimum of 9 steps
        self.__step = max(1, self.degree // steps)  # Ensure step is at least 1 degree

    @GObject.Property
    def degree(self) -> int:
        """
        - optional, read-write

        The target rotation degree.
        Must be > 0.

        Default: ``90``.
        """
        return self._degree

    @degree.setter
    def degree(self, value: int) -> None:
        self._degree = value
        self.__update_step()

    @GObject.Property
    def time(self) -> int:
        """
        - optional, read-write

        Rotation time in milliseconds.

        Default: ``135``.
        """
        return self._time

    @time.setter
    def time(self, value: int) -> None:
        self._time = value
        self.__update_step()

    @GObject.Property
    def direction(self) -> str:
        """
        - optional, read-write

        The direction of the arrow.
        Do not use this property if using custom icon name.

        Default: ``right``.

        Direction:
            - right
            - left
            - up
            - down
        """
        return self._direction

    @direction.setter
    def direction(self, value: str) -> None:
        self._direction = value
        self.icon_name = DIRECTION[value]

    @GObject.Property
    def counterclockwise(self) -> bool:
        """
        - optional, read-write

        Whether to rotate counterclockwise.

        Default: ``False``.
        """
        return self._counterclockwise

    @counterclockwise.setter
    def counterclockwise(self, value: bool) -> None:
        self._counterclockwise = value

    def toggle(self) -> None:
        """
        Rotate arrow.
        """
        self.rotated = not self._rotated
