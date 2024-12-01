from typing import Union
from gi.repository import Gdk  # type: ignore
from ignis.exceptions import DisplayNotFoundError


def get_monitor(monitor_id: int) -> Union[Gdk.Monitor, None]:
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
