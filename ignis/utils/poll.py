from ignis.gobject import IgnisGObject
from gi.repository import GLib, GObject  # type: ignore
from typing import Any, Callable


class Poll(IgnisGObject):
    """
    Calls a callback every n milliseconds specified by the timeout.

    You can pass arguments to the constructor, and they will be passed to the callback.

    Example usage:

    .. code-block:: python

        from ignis.utils import Utils

        # print "Hello" every second
        Utils.Poll(timeout=1_000, callback=lambda self: print("Hello"))
    """

    def __init__(self, timeout: int, callback: Callable, *args):
        super().__init__()
        self._id: int | None = None
        self._output: Any = None

        self._timeout = timeout
        self._callback = callback
        self._args = args

        self.__main()

    @GObject.Signal
    def changed(self):
        """
        - Signal

        Emitted at each iteration.
        """

    @GObject.Property
    def timeout(self) -> int:
        """
        - required, read-write

        The timeout interval in milliseconds.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, value: int) -> None:
        self._timeout = value

    @GObject.Property
    def callback(self) -> Callable:
        """
        - required, read-write

        The function to call when the timeout is reached. The ``self`` will passed as an argument.
        """
        return self._callback

    @callback.setter
    def callback(self, value: Callable) -> None:
        self._callback = value

    @GObject.Property
    def output(self) -> Any:
        """
        - not argument, read-only

        The output of the callback.

        .. hint::
            You can use bind() on ``output``.
        """
        return self._output

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
