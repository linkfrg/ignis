from ignis.gobject import IgnisGObject
from typing import Any


class HyprlandObject(IgnisGObject):
    def __init__(self, match_dict: dict[str, Any] | None = None):
        super().__init__()
        if match_dict is None:
            match_dict = {}
        self._match_dict = match_dict

    def _sync(self, data: dict[str, Any]) -> None:
        for key, value in data.items():
            prop_name = self._match_dict.get(key, key)
            if value != getattr(self, f"_{prop_name}"):
                setattr(self, f"_{prop_name}", value)
                self.notify(prop_name)
