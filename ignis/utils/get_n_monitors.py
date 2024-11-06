from gi.repository import Gdk  # type: ignore
from ignis.exceptions import DisplayNotFoundError


def get_n_monitors() -> int:
    """
    Get the number of monitors.

    Returns:
        The number of monitors.
    """
    display = Gdk.Display.get_default()
    if not display:
        raise DisplayNotFoundError()

    return len(display.get_monitors())
