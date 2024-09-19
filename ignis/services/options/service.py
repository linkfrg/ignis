import sys
import json
from typing import Any
from ignis.exceptions import OptionsGroupExistsError, OptionsGroupNotFoundError
from gi.repository import GObject  # type: ignore
from ignis.base_service import BaseService
from .constants import OPTIONS_FILE
from .group import OptionsGroup

class OptionsService(BaseService):
    """
    Service to manage options.
    This service stores options and their values in the ``~/.cache/ignis/options.json`` file.

    .. warning::
        You should not manually edit the ``~/.cache/ignis/options.json`` file.
        Use this service instead.


    **Example usage:**

    .. code-block:: python

        from ignis.services.options import OptionsService

        options = OptionsService.get_default()

        SOME_OPTION = "some_option"

        options.create_option(name=SOME_OPTION, default="hi", exists_ok=True)
        options.set_option(SOME_OPTION, "bye")

        print(options.get_option(SOME_OPTION))

    """

    def __init__(self):
        super().__init__()
        self._groups: dict[str, OptionsGroup] = {}
        self.__load_groups()

    def __load_groups(self) -> None:
        if "sphinx" in sys.modules:
            return

        try:
            with open(OPTIONS_FILE) as file:
                data = json.load(file)

                for i in data.keys():
                    self._groups[i] = self.__init_group(name=i, data=data.get(i, None))

        except FileNotFoundError:
            with open(OPTIONS_FILE, "w") as file:
                json.dump({}, file)

    def __sync(self) -> None:
        with open(OPTIONS_FILE, "w") as file:
            json.dump(self.data, file, indent=2)

        self.notify("data")


    def create_group(self, name: str, exists_ok: bool = False) -> OptionsGroup:
        group = self._groups.get(name, None)
        if not group:
            new_group = self.__init_group(name=name)
            self._groups[name] = new_group
            self.__sync()
            self.notify("groups")
            return new_group
        else:
            if exists_ok:
                return group
            else:
                raise OptionsGroupExistsError(name)

    def get_group(self, name: str) -> OptionsGroup:
        group = self._groups.get(name, None)

        if group:
            return group
        else:
            raise OptionsGroupNotFoundError(name)

    def __remove_group(self, group: OptionsGroup) -> None:
        self._groups.pop(group.name)
        self.__sync()
        self.notify("groups")
        self.notify("data")

    def __init_group(self, name: str, data: dict[str, Any] | None = None) -> OptionsGroup:
        group = OptionsGroup(name=name, data=data)
        group.connect("removed", self.__remove_group)
        group.connect("changed", lambda x: self.__sync())
        return group

    @GObject.Property
    def groups(self) -> dict[str, OptionsGroup]:
        return self._groups

    @GObject.Property
    def data(self) -> dict[str, Any]:
        return {key: group.data for key, group in self._groups.items()}

