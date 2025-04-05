from ignis.gobject import IgnisGObject, IgnisProperty
from gi.repository import Gio  # type: ignore
from collections.abc import Callable
from ignis.app import IgnisApp
from typing import TypeAlias

app = IgnisApp.get_default()

ItemsType: TypeAlias = "list[IgnisMenuItem | IgnisMenuModel | IgnisMenuSeparator]"


class IgnisMenuItem(IgnisGObject):
    """
    A menu item.

    Args:
        label: The label of item.
        enabled: Whether the item is enabled. If ``False``, the item cannot be selected.
        on_activate: The function to call when the user clicks on the item.
    """

    def __init__(
        self,
        label: str,
        enabled: bool = True,
        on_activate: Callable | None = None,
    ):
        super().__init__()
        self._label = label
        self._enabled = enabled
        self._on_activate = on_activate
        self._uniq_name = hex(id(self))

        action = Gio.SimpleAction.new(self._uniq_name, None)
        action.set_enabled(enabled)
        action.connect("activate", self.__on_activate)

        app.add_action(action)

    @IgnisProperty
    def label(self) -> str:
        """
        The label of item.
        """
        return self._label

    @IgnisProperty
    def uniq_name(self) -> str:
        """
        The unique name of the ``Gio.Action``.
        """
        return self._uniq_name

    @IgnisProperty
    def action_name(self) -> str:
        """
        The full action name (``app.UNIQ_NAME``).
        """
        return f"app.{self.uniq_name}"

    @IgnisProperty
    def enabled(self) -> bool:
        """
        Whether the item is enabled. If ``False``, the item cannot be selected.
        """
        return self._enabled

    @IgnisProperty
    def on_activate(self) -> Callable:
        """
        The function to call when the user clicks on the item.
        """
        return self._on_activate

    @on_activate.setter
    def on_activate(self, value: Callable) -> None:
        self._on_activate = value

    def __on_activate(self, *args) -> None:
        if self.on_activate:
            self.on_activate(self)


class IgnisMenuSeparator:
    """
    A simple object representing a menu separator.
    """


class IgnisMenuModel(IgnisGObject):
    """
    A helper class that provides a convenient way to construct a :class:`Gio.Menu`.

    Args:
        *args: Items to add.
        label: The label of the submenu. Only works if this model passed as an item of the parent model. Must be provided only as a **keyword** argument.

    .. code-block:: python

        from ignis.menu_model import IgnisMenuModel, IgnisMenuItem, IgnisMenuSeparator

        model = IgnisMenuModel(
            IgnisMenuItem(
                label="Item 1",
                on_activate=lambda x: print("item 1 activated!"),
            ),
            IgnisMenuItem(
                label="This is disabled item",
                enabled=False,
                on_activate=lambda x: print(
                    "you will not see this message in terminal hehehehehe"
                ),
            ),
            IgnisMenuModel(
                *(  # unpacking because items must be passed as *args
                    IgnisMenuItem(
                        label=str(i),
                        on_activate=lambda x, i=i: print(f"Clicked on item {i}!"),
                    )
                    for i in range(10)
                ),
                label="Submenu",  # pass label as keyword argument
            ),
        )

        # Access built Gio.Menu
        print(model.gmenu)

        # Generate Gio.Menu using classmethod
        IgnisMenuModel.generate_gmenu(
            items=[
                ...
            ]
        )
    """

    def __init__(
        self,
        *args: "IgnisMenuItem | IgnisMenuModel | IgnisMenuSeparator",
        label: str | None = None,
    ):
        super().__init__()
        self._gmenu: Gio.Menu | None = None
        self._items: ItemsType = []

        self._label = label
        self.items = args

    @IgnisProperty
    def items(self) -> ItemsType:
        """
        A list of items.
        """
        return self._items

    @items.setter
    def items(self, value: ItemsType) -> None:
        self._items = value
        self._gmenu = self.generate_gmenu(value)

    @IgnisProperty
    def gmenu(self) -> "Gio.Menu | None":
        """
        The `Gio.Menu` built from the contents of :attr:`items`, or ``None`` if no items are present.
        """
        return self._gmenu

    @IgnisProperty
    def label(self) -> str | None:
        """
        The label of the submenu. Only Works if this model passed as an item of the parent model.
        """
        return self._label

    @classmethod
    def generate_gmenu(cls, items: ItemsType) -> Gio.Menu:
        """
        Generate :class:`Gio.Menu` from the given ``items``.

        Args:
            items: A list of items.

        Returns:
            Generated :class:`Gio.Menu`.
        """
        root_menu = Gio.Menu()
        current_section = Gio.Menu()
        root_menu.append_section(None, current_section)

        for item in items:
            if isinstance(item, IgnisMenuItem):
                current_section.append(item.label, item.action_name)

            elif isinstance(item, IgnisMenuModel):
                current_section.append_submenu(item.label, item.gmenu)

            elif isinstance(item, IgnisMenuSeparator):
                current_section = Gio.Menu()
                root_menu.append_section(None, current_section)

        return root_menu
