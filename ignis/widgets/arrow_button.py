from ignis.widgets.button import Button
from ignis.widgets.arrow import Arrow

class ArrowButton(Button):
    """
    Bases: :class:`~ignis.widgets.button.Button`.

    Simple button with arrow. On click will toggle (rotate) arrow.

    Properties:
        - **arrow** (:class:`~ignis.widgets.Widget.Arrow`, required, read-only): An arrow instance.

    .. code-block:: python

        Widget.ArrowButton(
            arrow=Widget.Arrow(
                ... # arrow specific properties goes here
            )
        )
    """

    __gtype_name__ = "IgnisArrowButton"

    def __init__(self, arrow: Arrow, **kwargs):
        self.__arrow = arrow

        super().__init__(child=self.__arrow, **kwargs)
        self.connect("clicked", lambda x: self.__arrow.toggle())

    def toggle(self) -> None:
        """
        Same as :func:`~ignis.widgets.Widget.Arrow.toggle`
        """
        self.__arrow.toggle()
