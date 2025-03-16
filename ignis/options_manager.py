import json
from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisGObject, Binding, IgnisProperty
from ignis.utils import Utils
from typing import Any
from collections.abc import Callable
from collections.abc import Generator
from ignis import is_sphinx_build


class Option(IgnisGObject):
    """
    :meta private:

    The class for simulating a GObject that represents an option and its value,
    need for OptionsGroup.bind()
    """

    def __init__(self, manager: "OptionsGroup", name: str):
        super().__init__()
        self._manager = manager
        self._name = name

        self._manager.connect("changed", self.__check)

    def __check(self, manager, name: str) -> None:
        if name == self._name:
            self.notify("value")

    @IgnisProperty
    def value(self):
        return getattr(self._manager, self._name)


class OptionsGroup(IgnisGObject):
    """
    An options group.
    """

    def __init__(self):
        super().__init__()
        self._modified_options: dict[str, Any] = {}

        for subgroup_name, subgroup in self.__yield_subgroups():
            subgroup.connect(
                "changed",
                lambda x, option_name, subgroup_name=subgroup_name: self.emit(
                    "subgroup-changed", subgroup_name, option_name
                ),
            )

    @GObject.Signal
    def changed(self, option_name: str):
        """
        - Signal

        Emitted when an option of this group has changed

        Args:
            option_name: The name of the option.
        """

    @GObject.Signal
    def subgroup_changed(self, subgroup_name: str, option_name: str):
        """
        - Signal

        Emitted when an option of a subgroup has changed

        Args:
            subgroup_name: The name of the subgroup.
            option_name: The name of the option.
        """

    def bind(self, property_name: str, transform: Callable | None = None) -> Binding:
        """
        :meta private:

        Creates a fake GObject that represents an option
        and makes Binding for it
        """
        opt_obj = Option(self, property_name.replace("-", "_"))
        return opt_obj.bind("value", transform)

    def connect_option(self, option_name: str, callback: Callable, *args) -> None:
        """
        Connect an option change event to the specified `callback`.

        This method serves as a replacement for the ``notify`` signal, as options are simple Python properties, not GObject properties.

        Args:
            option_name: The name of the option to connect.
            callback: The function to invoke when the value of the option changes.

        Any ``*args`` will be passed to the ``callback``.
        """
        option_name = option_name.replace("-", "_")
        self.connect(
            "changed", lambda x, name: callback(*args) if option_name == name else None
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary representation of all options and subgroups.
        """
        data = self._modified_options.copy()
        for name, manager in self.__yield_subgroups():
            data[name] = manager.to_dict()

        return data

    def _reload(self, data: dict[str, Any]) -> None:
        for key, value in data.items():
            if not hasattr(self, key):
                continue
            attr = getattr(self, key)
            if isinstance(attr, OptionsGroup):
                attr._reload(data[key])
            else:
                if attr != value:
                    setattr(self, key, value)

    def apply_from_dict(self, data: dict[str, Any]) -> None:
        """
        Apply values to options from a dictionary.

        Args:
            data: A dictionary containing the values to apply.
        """
        for key, value in data.items():
            if not hasattr(self, key):
                continue
            if isinstance(value, dict) and isinstance(getattr(self, key), OptionsGroup):
                getattr(self, key).apply_from_dict(value)
            else:
                self.__setattr__(key, value, False)

    def __yield_subgroups(
        self,
    ) -> Generator[tuple[str, "OptionsGroup"], None, None]:
        for key, value in type(self).__dict__.items():
            if key.startswith("__"):
                continue
            if isinstance(value, OptionsGroup):
                yield key, value

    def __setattr__(self, name: str, value: Any, emit: bool = True) -> None:
        if not name.startswith("_"):
            self._modified_options[name] = value
            if emit:
                self.emit("changed", name)
        return super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("set_"):
            property_name = name.replace("set_", "")
            if hasattr(self, property_name):
                return lambda value: setattr(self, property_name, value)
        elif name.startswith("get_"):
            property_name = name.replace("get_", "")
            if hasattr(self, property_name):
                return lambda: getattr(self, property_name)

        return super().__getattribute__(name)


class OptionsManager(OptionsGroup):
    """
    Bases: :class:`OptionsGroup`.

    This is the top-level class in the option structure.
    It provides support for loading and saving options to a file.
    Has support for hot-reloading when the file is modified externally.

    Args:
        file: The path to the file used for saving and loading options. Cannot be changed after initialization.
        hot_reload: Whether to enable hot-reloading.

    The standard option structure must follow this format:

    .. code-block:: python

        from ignis.options_manager import OptionsManager, OptionsGroup

        class SomeOptions(OptionsManager):
            def __init__(self):
                super().__init__(file="PATH/TO/FILE")

            class Subgroup1(OptionsGroup):
                option1: bool = False
                option2: int = 5000

            class SomeSubgroup(OptionsGroup):
                example_option: str | None = get_something...()
                test: str = "%Y-%m-%d_%H-%M-%S.mp4"


            subgroup1 = Subgroup1()
            some_subgroup = SomeSubgroup()

        some_options = SomeOptions()

    """

    def __init__(self, file: str | None = None, hot_reload: bool = True):
        super().__init__()
        self._file = file

        if not is_sphinx_build and self._file is not None:
            self.connect("changed", self.__autosave)
            self.connect("subgroup-changed", self.__autosave)

            self.load_from_file(self._file)

            if hot_reload:
                Utils.FileMonitor(path=self._file, callback=self.__hot_reload)

    def __hot_reload(self, x, path: str, event_type: str) -> None:
        if not self._file:
            return

        if event_type != "changes_done_hint":
            return

        with open(self._file) as fp:
            data = json.load(fp)

        self._reload(data)

    def __autosave(self, *args) -> None:
        self.save_to_file(self._file)  # type: ignore

    def save_to_file(self, file: str) -> None:
        """
        Manually save options to the specified file.

        Args:
            file: The path to the file where options will be saved.
        """
        with open(file, "w") as fp:
            json.dump(self.to_dict(), fp, indent=4)

    def load_from_file(self, file: str) -> None:
        """
        Manually load options from the specified file.

        Args:
            file: The path to the file from which options will be loaded.
        """
        with open(file) as fp:
            data = json.load(fp)
            self.apply_from_dict(data)
