from ignis.gobject import IgnisGObject
from typing import TypeVar

T = TypeVar("T", bound="BaseService")


class BaseService(IgnisGObject):
    """
    Bases: :class:`~ignis.gobject.IgnisGObject`.

    The base class for all services.
    """

    _instance: T | None = None  # type: ignore

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def get_default(cls: type[T]) -> T:
        """
        Returns the default Service object for this process, creating it if necessary.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
