from gi.repository import Gdk, Gio  # type: ignore
from ignis.exceptions import DisplayNotFoundError


def get_monitors() -> Gio.ListModel:
    """
    Get a list model of :class:`Gdk.Monitor`.

    Returns:
        A list model of :class:`Gdk.Monitor`.
    """
    display = Gdk.Display.get_default()
    if not display:
        raise DisplayNotFoundError()
    return display.get_monitors()
