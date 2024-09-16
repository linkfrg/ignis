from gi.repository import GObject, Gio  # type: ignore
from ignis.gobject import IgnisGObject


class ApplicationAction(IgnisGObject):
    """
    Application action.

    Properties:
        - **action** (``str``, read-only): ID of the action.
        - **name** (``str``, read-only): Human-readable name of the action.
    """

    def __init__(self, app: Gio.DesktopAppInfo, action: str):
        super().__init__()

        self._app = app
        self._action = action
        self._name: str = app.get_action_name(action)

    @GObject.Property
    def action(self) -> str:
        return self._action

    @GObject.Property
    def name(self) -> str:
        return self._name

    def launch(self) -> None:
        """
        Launch action.
        """
        self._app.launch_action(self.action, None)
