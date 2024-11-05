from gi.repository import GObject, Gio  # type: ignore
from ignis.gobject import IgnisGObject


class ApplicationAction(IgnisGObject):
    """
    Application action.
    """

    def __init__(self, app: Gio.DesktopAppInfo, action: str):
        super().__init__()

        self._app = app
        self._action = action
        self._name: str = app.get_action_name(action)

    @GObject.Property
    def action(self) -> str:
        """
        - read-only

        The ID of the action.
        """
        return self._action

    @GObject.Property
    def name(self) -> str:
        """
        - read-only

        The human-readable name of the action.
        """
        return self._name

    def launch(self) -> None:
        """
        Launch this action.
        """
        self._app.launch_action(self.action, None)
