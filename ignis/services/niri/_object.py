from ignis.gobject import IgnisGObject
from typing import Any


class NiriObject(IgnisGObject):
    def __init__(self, match_dict: dict[str, Any] | None = None):
        super().__init__()
        if match_dict is None:
            match_dict = {}
        self._match_dict = match_dict

    def _sync(self, data: dict[str, Any]) -> None:
        for key, value in data.items():
            public_prop_name = self._match_dict.get(key, key)
            protected_prop_name = f"_{public_prop_name}"

            if not hasattr(self, protected_prop_name):
                continue

            if value != getattr(self, protected_prop_name):
                setattr(self, protected_prop_name, value)
                self.notify(public_prop_name)
