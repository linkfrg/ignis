from ignis.widgets.button import Button
from ignis.widgets.arrow import Arrow


class ArrowButton(Button):
    """
    Bases: :class:`~ignis.widgets.button.Button`.

    A simple button with an arrow. On click, it will toggle (rotate) the arrow.

    Properties:
        - **arrow** (:class:`~ignis.widgets.Widget.Arrow`, required, read-only): An instance of an arrow.

    .. code-block:: python

        Widget.ArrowButton(
            arrow=Widget.Arrow(
                ... # Arrow-specific properties go here
            )
        )
    """

    __gtype_name__ = "IgnisArrowButton"

    def __init__(self, arrow: Arrow, **kwargs):
        self._arrow = arrow

        super().__init__(child=self._arrow, **kwargs)
        self.connect("clicked", lambda x: self._arrow.toggle())

    def toggle(self) -> None:
        """
        Same as :func:`~ignis.widgets.Widget.Arrow.toggle`
        """
        self._arrow.toggle()
