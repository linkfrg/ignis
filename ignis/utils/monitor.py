from gi.repository import Gdk, Gio  # type: ignore
from ignis.exceptions import DisplayNotFoundError


def get_monitor(monitor_id: int) -> "Gdk.Monitor | None":
    """
    Get the ``Gdk.Monitor`` by its ID.

    Args:
        monitor_id: The ID of the monitor.

    Returns:
        The monitor with the given ID, or ``None`` if no such monitor exists.
    """
    display = Gdk.Display.get_default()
    if not display:
        raise DisplayNotFoundError()

    return display.get_monitors().get_item(monitor_id)  # type: ignore


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
