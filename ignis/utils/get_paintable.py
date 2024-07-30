from gi.repository import Gtk, Gdk, Gio


def get_paintable(widget: Gtk.Widget, icon_name: str, size: int) -> Gdk.Paintable:
    """
    Get a ``Gdk.Paintable`` by icon name.

    Args:
        widget (``Gtk.Widget``): The parent widget.
        icon_name (``str``): The name of the icon to look up.
        size (``int``): The size of the icon.

    Returns:
        ``Gdk.Paintable``: The paintable object for the icon.
    """
    icon = Gio.ThemedIcon.new(icon_name)
    icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
    return icon_theme.lookup_by_gicon(
        icon, size, widget.get_scale_factor(), widget.get_direction(), 0
    )
