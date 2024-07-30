from gi.repository import Gdk

def get_monitor(monitor_id: int) -> Gdk.Monitor:
    """
    Get the ``Gdk.Monitor`` by its ID.

    Args:
        monitor_id (``int``): The ID of the monitor.

    Returns:
        ``Gdk.Monitor`` or ``None``: The monitor with the given ID, or ``None`` if no such monitor exists.
    """
    return Gdk.Display.get_default().get_monitors().get_item(monitor_id)
