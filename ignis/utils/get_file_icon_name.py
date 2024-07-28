from gi.repository import Gio


def get_file_icon_name(path: str, symbolic: bool = False) -> str:
    """ 
    Get a standart icon name for the file or directory.

    Args:
        path (``str``): The path to the file or directory.
        symbolic (``bool``, optional): Whether the icon should be symbolic.

    Returns:
        ``str``: The name of the icon.
    """
    file = Gio.File.new_for_path(path)
    icons = (
        file.query_info("standard::icon", Gio.FileQueryInfoFlags.NONE)
        .get_icon()
        .get_names()
    )
    if symbolic:
        for icon in icons:
            if icon.endswith("-symbolic"):
                return icon
    else:
        return icons[0] if len(icons) > 0 else None
