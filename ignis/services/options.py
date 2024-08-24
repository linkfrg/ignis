import sys
import json
from ignis.gobject import IgnisGObject, Binding
from gi.repository import GObject
from typing import Any
from ignis.settings import CACHE_DIR
from ignis.exceptions import OptionExistsError, OptionNotFoundError

OPTIONS_FILE = f"{CACHE_DIR}/options.json"


class Option(IgnisGObject):
    """
    :meta private:
    """

    def __init__(self, name: str, value: Any = None):
        super().__init__()
        self._name = name
        self._value = value

    @GObject.Property
    def name(self) -> str:
        return self._name

    @GObject.Property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value


class OptionsService(IgnisGObject):
    """
    Service to manage options.
    This service stores options and their values in the ``~/.cache/ignis/options.json`` file.

    .. warning::
        You should not manually edit the ``~/.cache/ignis/options.json`` file.
        Use this service instead.


    **Example usage:**

    .. code-block:: python

        from ignis.services import Service

        options = Service.get("options")

        SOME_OPTION = "some_option"

        options.create_option(name=SOME_OPTION, default="hi", exists_ok=True)
        options.set_option(SOME_OPTION, "bye")

        print(options.get_option(SOME_OPTION))

    """

    def __init__(self):
        super().__init__()
        self.__data = {}
        self.__load_data()

    def __load_data(self) -> dict:
        if 'sphinx' in sys.modules:
            return

        empty = {}
        try:
            with open(OPTIONS_FILE) as file:
                data = json.load(file)

                for i in data.keys():
                    self.__data[i] = Option(name=i, value=data[i])

        except FileNotFoundError:
            with open(OPTIONS_FILE, "w") as file:
                json.dump(empty, file)

    def __sync(self) -> None:
        json_dict = {}

        for key, option in self.__data.items():
            json_dict[key] = option.value

        with open(OPTIONS_FILE, "w") as file:
            json.dump(json_dict, file, indent=2)

    def create_option(self, name: str, default: Any, exists_ok: bool = False) -> None:
        """
        Create an option.

        Args:
            name (``str``): The name of the option.
            default (``Any``): The default value for the option.
            exists_ok (``bool``, optional): If ``True``, do not raise ``OptionExistsError`` if the option already exists. Default: ``False``.

        Raises:
            OptionExistsError: If the option already exists and ``exists_ok`` is set to ``False``.
        """

        option = self.__data.get(name, None)
        if not option:
            self.__data[name] = Option(name=name, value=default)
            self.__sync()
        else:
            if not exists_ok:
                raise OptionExistsError(name)

    def remove_option(self, name: str) -> None:
        """
        Remove an option.

        Args:
            name (``str``): The name of the option to be removed.

        Raises:
            OptionNotFoundError: If the option does not exist.
        """
        option = self.__data.get(name, None)
        if option:
            self._data.pop(name)
        else:
            raise OptionNotFoundError(name)

    def get_option(self, name: str) -> Any:
        """
        Retrieve the value of an option by its name.

        Args:
            name (``str``): The name of the option.

        Returns:
            The value of the option.

        Raises:
            OptionNotFoundError: If the option does not exist.
        """
        option = self.__data.get(name, None)

        if option:
            return option.value
        else:
            raise OptionNotFoundError(name)

    def set_option(self, name: str, value: Any) -> None:
        """
        Set the value of an option by its name.

        Args:
            name (``str``): The name of the option.
            value (``Any``): The value to set for the option.
        Raises:
            OptionNotFoundError: If the option does not exist.
        """
        option = self.__data.get(name, None)
        if option:
            option.value = value
        else:
            raise OptionNotFoundError(name)
        self.__sync()

    def bind_option(self, name: str, transform: callable = None) -> Binding:
        """
        Like ``bind()``, but for option.

        Args:
            name (``str``): The name of the option to bind.
            transform (``callable``, optional): A transform function.

        Returns:
            ``Binding``.

        Raises:
            OptionNotFoundError: If the option does not exist.
        """
        option = self.__data.get(name, None)
        if not option:
            raise OptionNotFoundError(name)

        return Binding(option, "value", transform)

    def connect_option(self, name: str, callback: callable) -> None:
        """
        Associate a callback function with changes to an option value.
        When the option value changes, the callback function will be invoked with the new value.

        Args:
            name (``str``): The name of the option.
            callback (``callable``): A function to call when the option value changes. The new value of the option will be passed to this function.

        Raises:
            OptionNotFoundError: If the option does not exist.
        """
        option = self.__data.get(name, None)
        if not option:
            raise OptionNotFoundError(name)

        option.connect("notify::value", lambda x, y: callback(option.value))
