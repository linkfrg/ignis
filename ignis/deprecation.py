"""Simple deprecation utilities."""

from loguru import logger
from collections.abc import Callable


logger.level("DEPRECATED", no=25)


def deprecation_warning(message: str) -> None:
    """
    Log a warning about the deprecation of a feature or function.

    Args:
        message: The message to print.
    """
    logger.log("DEPRECATED", message)


def deprecated_func(message: str):
    """
    A decorator to mark a function as deprecated.

    Args:
        message: The message to log. ``{name}`` will be replaced with the function name.
    """

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            deprecation_warning(message.replace("{name}", func.__name__))
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecated_class(message: str):
    """
    A decorator to mark a class as deprecated.

    Args:
        message: The message to log. ``{name}`` will be replaced with the class name.
    """

    def decorator(cls):
        deprecation_warning(message.replace("{name}", cls.__name__))
        return cls

    return decorator
