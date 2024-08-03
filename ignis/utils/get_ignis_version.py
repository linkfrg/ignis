from ignis.version import __version__, __commit__

def get_ignis_version() -> str:
    """
    Get the current Ignis version.

    Returns:
        ``str``: The Ignis version.
    """
    return __version__


def get_ignis_commit() -> str:
    """
    Get the current Ignis commit hash.

    Returns:
        ``str``: The Ignis commit hash.
    """
    return __commit__
