from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisGObject
from typing import Callable
from .thread import run_in_thread


class ThreadTask(IgnisGObject):
    """
    Execute a function in another thread and call a callback when it's finished.
    The output from the function is passed to the callback.

    Signals:
        - finished (``Any``): Emitted when the function has finished. Passes the output from the function as an argument.

    Parameters:
        target (``Callable``): The function to execute in another thread.
        callback (``Callable``): The function to call when ``target`` has finished.

    """

    __gsignals__ = {
        "finished": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (object,)),
    }

    def __init__(self, target: Callable, callback: Callable):
        super().__init__()
        self._target = target
        self._callback = callback

        self.connect("finished", lambda x, result: callback(result))
        self.__run()

    @run_in_thread
    def __run(self) -> None:
        result = self._target()
        self.emit("finished", result)
