from ignis.gobject import IgnisProperty, DataGObject


class NiriOutput(DataGObject):
    """
    An output.
    """

    def __init__(self):
        super().__init__()
        self._name: str = ""
        self._make: str = ""
        self._model: str = ""

    @IgnisProperty
    def name(self) -> str:
        """
        - read-only

        Name of the output (eg. eDP-1).
        """
        return self._name

    @IgnisProperty
    def make(self) -> str:
        """
        - read-only

        Manufacturer of the output.
        """
        return self._make

    @IgnisProperty
    def model(self) -> str:
        """
        - read-only

        Model name of the output.
        """
        return self._model
