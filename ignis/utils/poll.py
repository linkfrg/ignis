from ignis.gobject import IgnisGObject
from gi.repository import GLib, GObject  # type: ignore
from typing import Any, Callable


class Poll(IgnisGObject):
    """
    Call a callback every n milliseconds specefied by the timeout.

    Properties:
        - **timeout** (``int``, required, read-write): The timeout interval in milliseconds.
        - **callback** (``Callable``, required, read-write): The function to call when the timeout is reached. The ``self`` will passed as an argument.
        - **output** (``str``, not argument, read-only): The output of the callback.

    You can pass arguments to the constructor, and they will be passed to the callback.

    .. hint::
        You can use bind() on ``output``.

    **Example usage:**

    .. code-block:: python

        from ignis.utils import Utils

        # print "Hello" every second
        Utils.Poll(timeout=1_000, callback=lambda self: print("Hello"))
    """

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, timeout: int, callback: Callable, *args):
        super().__init__()
        self._id: int | None = None
        self._output: Any = None

        self._timeout = timeout
        self._callback = callback
        self._args = args

        self.__main()

    @GObject.Property
    def output(self) -> Any:
        return self._output

    @GObject.Property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, value: int) -> None:
        self._timeout = value

    @GObject.Property
    def callback(self) -> Callable:
        return self._callback

    @callback.setter
    def callback(self, value: Callable) -> None:
        self._callback = value

    def __main(self) -> None:
        self._output = self._callback(self, *self._args)
        self.emit("changed")
        self.notify("output")
        self._id = GLib.timeout_add(self._timeout, self.__main)

    def cancel(self) -> None:
        """
        Cancel polling.
        """
        if not self._id:
            return

        if GLib.MainContext.default().find_source_by_id(self._id):
            GLib.source_remove(self._id)
