from ignis.gobject import IgnisGObject
from gi.repository import GObject  # type: ignore
from ignis.exceptions import OptionExistsError, OptionNotFoundError
from .option import Option
from typing import Any


class OptionsGroup(IgnisGObject):
    """
    An options group.

    .. warning::
        You shouldn't initialize this class manually.
        Use the :func:`~ignis.services.options.OptionsService.create_group` method instead.
    """

    def __init__(self, name: str, data: dict[str, Any] | None = None):
        super().__init__()
        self._name = name
        self._data: dict[str, Any] = {}

        if data:
            self.__load_data(data)

    def __load_data(self, data: dict[str, Any]) -> None:
        if not isinstance(data, dict):
            return

        for key in data.keys():
            self._data[key] = self.__init_option(name=key, value=data.get(key, None))

    @GObject.Signal
    def changed(self):
        """
        - Signal

        Emitted when options in this group is changed.
        """

    @GObject.Signal
    def removed(self):
        """
        - Signal

        Emitted when this options group is removed.
        """

    @GObject.Property
    def name(self) -> str:
        """
        - read-only

        The name of the group.
        """
        return self._name

    @GObject.Property
    def data(self) -> dict[str, Any]:
        """
        - read-only

        The dictionary containing all options and their values.
        """
        return {key: option.value for key, option in self._data.items()}

    def create_option(self, name: str, default: Any, exists_ok: bool = False) -> Option:
        """
        Create an option.

        Args:
            name: The name of the option.
            default: The default value for the option.
            exists_ok: If ``True``, do not raise :class:`~ignis.exceptions.OptionExistsError` if the option already exists. Default: ``False``.

        Returns:
            :class:`~ignis.services.options.Option`: The newly created option or already existing option.

        Raises:
            OptionExistsError: If the option already exists and ``exists_ok`` is set to ``False``.
        """

        option = self._data.get(name, None)
        if not option:
            new_option = self.__init_option(name=name, value=default)
            self._data[name] = new_option
            self.__sync()
            return new_option
        else:
            if not exists_ok:
                raise OptionExistsError(name)
            else:
                return option

    def get_option(self, name: str) -> Option:
        """
        Get ``Option`` object by its name.

        Args:
            name: The name of the option.

        Returns:
            :class:`~ignis.services.options.Option`: The option instance.

        Raises:
            OptionNotFoundError: If the option does not exist.
        """
        option = self._data.get(name, None)

        if option:
            return option
        else:
            raise OptionNotFoundError(name)

    def remove(self) -> None:
        """
        Remove this options group.
        """

        self.emit("removed")

    def __sync(self) -> None:
        self.emit("changed")

    def __remove_option(self, option: Option) -> None:
        option = self._data.get(option.name, None)
        if option:
            self._data.pop(option.name)
            self.__sync()

    def __init_option(self, name: str, value: Any = None) -> Option:
        option = Option(name=name, value=value)
        option.connect("notify::value", lambda x, y: self.__sync())
        option.connect("removed", lambda x, y: self.__remove_option(option))
        return option
