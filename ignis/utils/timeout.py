from gi.repository import GLib, GObject
from ignis.gobject import IgnisGObject


class Timeout(IgnisGObject):
    """
    Call a function after a specified interval of time.

    Properties:
        - **ms** (``int``, required, read-only): Time in milliseconds.
        - **target** (``callable``, required, read-only): Function to call.

    **Example usage:**

    .. code-block:: python

        from ignis.utils import Utils

        Utils.Timeout(ms=3000, target=lambda: print("Hello"))
    """

    def __init__(self, ms: int, target: callable, *args):
        super().__init__()
        self._ms = ms
        self._target = target
        self._id = GLib.timeout_add(ms, target, *args)

    @GObject.Property
    def ms(self) -> int:
        return self._ms

    @GObject.Property
    def target(self) -> callable:
        return self._target

    def cancel(self) -> None:
        """
        Cancel the timeout if it is active.

        This method prevents the ``target`` function from being called.
        """
        if GLib.MainContext.default().find_source_by_id(self._id):
            GLib.source_remove(self._id)
