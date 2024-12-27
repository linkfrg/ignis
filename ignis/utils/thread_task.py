from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisGObject
from typing import Callable
from .thread import run_in_thread


class ThreadTask(IgnisGObject):
    """
    Execute a function in another thread and call a callback when it's finished.
    The output from the function is passed to the callback.

    Parameters:
        target: The function to execute in another thread.
        callback: The function to call when ``target`` has finished.
    """

    def __init__(self, target: Callable, callback: Callable):
        super().__init__()
        self._target = target
        self._callback = callback

        self.connect("finished", lambda x, result: callback(result))

    @run_in_thread
    def __run(self) -> None:
        result = self._target()
        self.emit("finished", result)

    @GObject.Signal(arg_types=(object,))
    def finished(self, *args):
        """
        - Signal

        Args:
            output (``Any``): The output from the function.
        """

    def run(self) -> None:
        """
        Run this task.
        """
        self.__run()
