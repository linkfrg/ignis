import sys
import json
from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisGObject, Binding
from typing import Any, Callable
from collections.abc import Generator


class Option(IgnisGObject):
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
    def __init__(self):
        super().__init__()
        self._modified_options: dict[str, Any] = {}

        for name, manager in self.__yield_subgroups():
            manager.connect("changed", lambda x, name: self.emit("changed", name))

    @GObject.Signal(arg_types=(str,))
    def changed(self, *args): ...

    def __setattr__(self, name: str, value: Any, emit: bool = True) -> None:
        if not name.startswith("_"):
            self._modified_options[name] = value
            if emit:
                self.emit("changed", name)
        return super().__setattr__(name, value)

    def bind(self, property_name: str, transform: Callable | None = None) -> Binding:
        opt_obj = Option(self, property_name)
        return Binding(opt_obj, "value", transform)

    def to_dict(self) -> dict:
        data = self._modified_options.copy()
        for name, manager in self.__yield_subgroups():
            data[name] = manager.to_dict()

        return data

    def apply_from_dict(self, data: dict) -> None:
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
    def __init__(self, file: str):
        super().__init__()
        self._file = file
        if "sphinx" not in sys.modules:
            self.connect("changed", self.__dump)
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
