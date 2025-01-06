import sys
import json
from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisGObject, Binding
from typing import Any, Callable
from collections.abc import Generator


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

    @GObject.Property
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

    @GObject.Signal(arg_types=(str,))
    def changed(self, *args):
        """
        - Signal

        Emitted when an option of this group has changed

        Args:
            option_name: The name of the option.
        """

    @GObject.Signal(arg_types=(str, str))
    def subgroup_changed(self, *args):
        """
        - Signal

        Emitted when an option of a subgroup has changed

        Args:
            subgroup_name: The name of the subgroup.
            option_name: The name of the option.
        """

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

    def bind(self, property_name: str, transform: Callable | None = None) -> Binding:
        """
        :meta private:

        Creates a fake GObject that represents an option
        and makes Binding for it
        """
        opt_obj = Option(self, property_name.replace("-", "_"))
        return Binding(opt_obj, "value", transform)

    def connect_option(self, option_name: str, callback: Callable, *args) -> None:
        """
        Connect an event of option change with the provided `callback`
        This method made as replacement for ``notify`` signal, since options are simple python properties and not GObject properties.

        Args:
            option_name: The name of the option to connect.
            callback: The callback to invoke when value of the option changes.

        `*args` will be passed to the `callback`.
        """
        option_name = option_name.replace("-", "_")
        self.connect(
            "changed", lambda x, name: callback(*args) if option_name == name else None
        )

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of all options and subgroups.
        """
        data = self._modified_options.copy()
        for name, manager in self.__yield_subgroups():
            data[name] = manager.to_dict()

        return data

    def apply_from_dict(self, data: dict) -> None:
        """
        Apply values for options from a dict.

        Args:
            data: A dict with values to apply.
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


class OptionsManager(OptionsGroup):
    """
    Bases: :class:`OptionsGroup`.

    This is the top-level class in the options hierarchy.

    The common options hierarchy must look like this:

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

    def __init__(self, file: str):
        super().__init__()
        self._file = file
        if "sphinx" not in sys.modules:
            self.connect("changed", self.__dump)
            self.connect("subgroup-changed", self.__dump)
            try:
                self.load(self._file)
            except json.decoder.JSONDecodeError:
                pass

    def __dump(self, *args) -> None:
        with open(self._file, "w") as file:
            json.dump(self.to_dict(), file, indent=4)

    def load(self, file: str) -> None:
        with open(file) as fp:
            data = json.load(fp)
            self.apply_from_dict(data)
