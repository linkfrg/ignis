import threading
from typing import Callable


def thread(target: Callable, *args, **kwargs) -> threading.Thread:
    """
    Simply run the given function in a thread.
    The provided args and kwargs will be passed to the function.

    Args:
        target: The function to run.

    Returns:
        The thread in which the function is running.
    """
    th = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
    th.start()
    return th


def run_in_thread(func: Callable) -> Callable:
    """
    Decorator to run the decorated function in a thread.
    """

    def wrapper(*args, **kwargs):
        return thread(func, *args, **kwargs)

    return wrapper
