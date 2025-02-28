from ignis.gobject import IgnisProperty
from typing import Any
from ._object import HyprlandObject

MATCH_DICT = {
    "class": "class_name",
    "initialClass": "initial_class",
    "initialTitle": "initial_title",
    "fullscreenClient": "fullscreen_client",
    "focusHistoryID": "focus_history_id",
    "inhibitingIdle": "inhibiting_idle",
}


class HyprlandWindow(HyprlandObject):
    """
    A window.
    """

    def __init__(self):
        super().__init__(match_dict=MATCH_DICT)

        self._address: str = ""
        self._mapped: bool = False
        self._hidden: bool = False
        self._at: tuple[int, int] = (-1, -1)
        self._size: tuple[int, int] = (-1, -1)
        self._workspace_id: int = -1
        self._workspace_name: str = ""
        self._floating: bool = False
        self._pseudo: bool = False
        self._monitor: int = -1
        self._class_name: str = ""
        self._title: str = ""
        self._initial_class: str = ""
        self._initial_title: str = ""
        self._pid: int = -1
        self._xwayland: bool = False
        self._pinned: bool = False
        self._fullscreen: int = -1
        self._fullscreen_client: int = -1
        self._grouped: list = []
        self._tags: list = []
        self._swallowing: str = ""
        self._focus_history_id: int = -1
        self._inhibiting_idle: bool = False

    def _sync(self, data: dict[str, Any]) -> None:
        workspace = data.pop("workspace", None)
        if workspace:
            data["workspace_id"] = workspace["id"]
            data["workspace_name"] = workspace["name"]
        super()._sync(data)

    @IgnisProperty
    def address(self) -> str:
        """
        - read-only

        The address of the window.
        """
        return self._address

    @IgnisProperty
    def mapped(self) -> bool:
        """
        - read-only

        Whether the window is mapped.
        """
        return self._mapped

    @IgnisProperty
    def hidden(self) -> bool:
        """
        - read-only

        Whether the window is hidden.
        """
        return self._hidden

    @IgnisProperty
    def at(self) -> tuple[int, int]:
        """
        - read-only

        The coordinates of the window (e.g., ``(1280, 920)``).
        """
        return self._at

    @IgnisProperty
    def size(self) -> tuple[int, int]:
        """
        - read-only

        The size of the window (e.g., ``(1280, 920)``).
        """
        return self._size

    @IgnisProperty
    def workspace_id(self) -> int:
        """
        - read-only

        The ID of the workspace where the window is placed.
        """
        return self._workspace_id

    @IgnisProperty
    def workspace_name(self) -> str:
        """
        - read-only

        The name of the workspace where the window is placed.
        """
        return self._workspace_name

    @IgnisProperty
    def floating(self) -> bool:
        """
        - read-only

        Whether the window is floating.
        """
        return self._floating

    @IgnisProperty
    def pseudo(self) -> bool:
        """
        - read-only

        Whether the window is pseudo.
        """
        return self._pseudo

    @IgnisProperty
    def monitor(self) -> int:
        """
        - read-only

        The ID of the monitor where the window is placed.
        """
        return self._monitor

    @IgnisProperty
    def class_name(self) -> str:
        """
        - read-only

        The class name of the window.
        """
        return self._class_name

    @IgnisProperty
    def title(self) -> str:
        """
        - read-only

        The title of the window.
        """
        return self._title

    @IgnisProperty
    def initial_class(self) -> str:
        """
        - read-only

        The initial class name of the window.
        """
        return self._initial_class

    @IgnisProperty
    def initial_title(self) -> str:
        """
        - read-only

        The initial title of the window.
        """
        return self._initial_title

    @IgnisProperty
    def pid(self) -> int:
        """
        - read-only

        The PID of the window.
        """
        return self._pid

    @IgnisProperty
    def xwayland(self) -> bool:
        """
        - read-only

        Whether the window is running through Xwayland.
        """
        return self._xwayland

    @IgnisProperty
    def pinned(self) -> bool:
        """
        - read-only

        Whether the window is pinned.
        """
        return self._pinned

    @IgnisProperty
    def fullscreen(self) -> int:
        """
        - read-only

        The fullscreen mode.
        """
        return self._fullscreen

    @IgnisProperty
    def fullscreen_client(self) -> int:
        """
        - read-only

        Fullscreen client.
        """
        return self._fullscreen_client

    @IgnisProperty
    def grouped(self) -> list:
        """
        - read-only

        Grouped.
        """
        return self._grouped

    @IgnisProperty
    def tags(self) -> list:
        """
        - read-only

        Tags.
        """
        return self._tags

    @IgnisProperty
    def swallowing(self) -> str:
        """
        - read-only

        Swallowing.
        """
        return self._swallowing

    @IgnisProperty
    def focus_history_id(self) -> int:
        """
        - read-only

        The focus history ID.
        """
        return self._focus_history_id

    @IgnisProperty
    def inhibiting_idle(self) -> bool:
        """
        - read-only

        The inhibiting idle status.
        """
        return self._inhibiting_idle
