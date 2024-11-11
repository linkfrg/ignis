import os
from gi.repository import Gio  # type: ignore


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
