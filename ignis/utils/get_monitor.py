from __future__ import annotations
from gi.repository import Gdk  # type: ignore
from ignis.exceptions import DisplayNotFoundError


def get_monitor(monitor_id: int) -> Gdk.Monitor | None:
    """
    Get the ``Gdk.Monitor`` by its ID.

    Args:
        monitor_id (``int``): The ID of the monitor.

    Returns:
        ``Gdk.Monitor | None``: The monitor with the given ID, or ``None`` if no such monitor exists.
    """
    display = Gdk.Display.get_default()
    if not display:
        raise DisplayNotFoundError()

    return display.get_monitors().get_item(monitor_id)  # type: ignore
