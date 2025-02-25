import os
from gi.repository import Gtk, Gdk, Gio  # type: ignore
from ignis.exceptions import DisplayNotFoundError


def get_paintable(
    widget: Gtk.Widget, icon_name: str, size: int
) -> "Gtk.IconPaintable | None":
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


def get_file_icon_name(path: str, symbolic: bool = False) -> str | None:
    """
    Get a standart icon name for the file or directory.

    Args:
        path: The path to the file or directory.
        symbolic: Whether the icon should be symbolic.

    Returns:
        The name of the icon. ``None`` if the icon with the given name is not found.
    """
    file = Gio.File.new_for_path(path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: {path}")
    info = file.query_info("standard::icon", Gio.FileQueryInfoFlags.NONE)
    icon_obj: Gio.ThemedIcon = info.get_icon()  # type: ignore
    icon_names = icon_obj.get_names()

    if symbolic:
        for icon in icon_names:
            if icon.endswith("-symbolic"):
                return icon

    if len(icon_names) > 0:
        return icon_names[0]

    return None
