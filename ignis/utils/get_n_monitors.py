from gi.repository import Gdk

def get_n_monitors() -> int:
    """
    Get the number of monitors.

    Returns:
        ``int``: The number of monitors.
    """
    return len(Gdk.Display.get_default().get_monitors())
