"""Simple deprecation utilities."""

import warnings
from collections.abc import Callable

# FIXME: make public someday
def _enable_deprecation_warnings() -> None:
    warnings.filterwarnings("default", category=DeprecationWarning)


def deprecation_warning(message: str) -> None:
    """
    Print a warning about deprecated features.

    Args:
        message: The message to print.
    """
    warnings.warn(message, DeprecationWarning, stacklevel=2)


def deprecated_func(message: str):
    """
    A decorator to mark a function as deprecated.

    Args:
        message: The warning message. ``{name}`` will be replaced with the function name.
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
        message: The warning message. ``{name}`` will be replaced with the class name.
    """

    def wrapper(cls):
        class DeprecatedMeta(type(cls)):  # type: ignore
            _warned = False

            def __getattribute__(self, name):
                if not DeprecatedMeta._warned:
                    deprecation_warning(message=message.format(name=cls.__name__))
                    DeprecatedMeta._warned = True

                return super().__getattribute__(name)

        return DeprecatedMeta(cls.__name__, cls.__bases__, dict(cls.__dict__))

    return wrapper
