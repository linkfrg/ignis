from gi.repository import Gtk, Gdk, Gio  # type: ignore
from ignis.exceptions import DisplayNotFoundError
from typing import Union


def get_paintable(
    widget: Gtk.Widget, icon_name: str, size: int
) -> Union[Gtk.IconPaintable, None]:
    """
    Get a ``Gdk.Paintable`` by icon name.

    Args:
        widget: The parent widget.
        icon_name: The name of the icon to look up.
        size: The size of the icon.

    Returns:
        The paintable object for the icon or ``None`` if no such icon exists.
    """
    display = Gdk.Display.get_default()
    if not display:
        raise DisplayNotFoundError()

    icon = Gio.ThemedIcon.new(icon_name)
    icon_theme = Gtk.IconTheme.get_for_display(display)
    return icon_theme.lookup_by_gicon(
        icon,
        size,
        widget.get_scale_factor(),
        widget.get_direction(),
        Gtk.IconLookupFlags.PRELOAD,
    )
