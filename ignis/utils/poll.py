from ignis.gobject import IgnisGObject
from gi.repository import GLib, GObject
from typing import Any


class Poll(IgnisGObject):
    """
    Call a callback every n seconds specefied by the timeout.

    Properties:
        - **timeout** (``int``, read-write): The timeout interval in seconds.
        - **callback** (``callable``, read-write): The function to call when the timeout is reached.
        - **output** (``str``, read-only): The output of the callback. This is not an argument for the constructor.

    You can pass arguments to the constructor, and they will be passed to the callback.

    **Example usage:**

        .. code-block:: python

            from ignis.utils import Utils

            # print "Hello" every second
            Utils.Poll(timeout=1, callback=lambda: print("Hello"))
    """

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, timeout: int, callback: callable, *args):
        super().__init__()
        self.__id = None

        self._output = None
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
    def callback(self) -> callable:
        return self._callback

    @callback.setter
    def callback(self, value: callable) -> None:
        self._callback = value

    def __main(self) -> None:
        self._output = self._callback(self, *self._args)
        self.emit("changed")
        self.notify("output")
        self.__id = GLib.timeout_add_seconds(self._timeout, self.__main)

    def cancel(self) -> None:
        """
        Cancel polling.
        """
        if GLib.MainContext.default().find_source_by_id(self.__id):
            GLib.source_remove(self.__id)
