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
    Service to manage options and options groups.
    This service stores options and their values in the ``~/.cache/ignis/options.json`` file.

    .. warning::
        You should not manually edit the ``~/.cache/ignis/options.json`` file.
        Use this service instead.

    Example usage:

    .. code-block:: python

        from ignis.services.options import OptionsService

        options = OptionsService.get_default()

        some_opt_group = options.create_group(name="some_group", exists_ok=True)

        some_option = some_opt_group.create_option(name="some_option", default="hi", exists_ok=True)
        some_option.set_value("bye")

        print(some_option.value)

        print(some_opt_group.data)

        print(options.data)

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

    @GObject.Property
    def groups(self) -> list[OptionsGroup]:
        """
        - read-only

        A list of all options groups.
        """
        return list(self._groups.values())

    @GObject.Property
    def data(self) -> dict[str, Any]:
        """
        - read-only

        The dictionary containing all options and their values from all groups.
        """
        return {key: group.data for key, group in self._groups.items()}

    def create_group(self, name: str, exists_ok: bool = False) -> OptionsGroup:
        """
        Create options group.

        Args:
            name: The name of the options group to create.
            exists_ok: If ``True``, do not raise :class:`~ignis.exceptions.OptionsGroupExistsError` if the group already exists. Default: ``False``.

        Returns:
            :class:`~ignis.services.options.OptionsGroup`: The newly created options group or already existing one.

        Raises:
            OptionsGroupExistsError: If the options group already exists and ``exists_ok`` is set to ``False``.
        """
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
        """
        Get ``OptionsGroup`` object by its name.

        Args:
            name: The name of the options group.

        Returns:
            :class:`~ignis.services.options.OptionsGroup`: The options group instance.

        Raises:
            OptionsGroupNotFoundError: If the options group does not exist.
        """
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

    def __init_group(
        self, name: str, data: dict[str, Any] | None = None
    ) -> OptionsGroup:
        group = OptionsGroup(name=name, data=data)
        group.connect("removed", self.__remove_group)
        group.connect("changed", lambda x: self.__sync())
        return group
