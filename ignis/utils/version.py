from ignis import __version__


def get_ignis_version() -> str:
    """
    Get the current Ignis version.

    Returns:
        The Ignis version.
    """
    return __version__


def get_ignis_commit() -> str:
    """
    Get the current Ignis commit hash.

    Returns:
        The Ignis commit hash.
    """

    try:
        from ignis.__commit__ import __commit__  # type: ignore

        return __commit__
    except (ImportError, ValueError):
        return ""


def get_ignis_branch() -> str:
    """
    Get the name of the current Ignis git branch.

    Returns:
        The name of the Ignis git branch.
    """
    try:
        from ignis.__commit__ import __branch__  # type: ignore

        return __branch__
    except (ImportError, ValueError):
        return ""


def get_ignis_commit_msg() -> str:
    """
    Get the message of the latest Ignis commit.

    Returns:
        The message of the latest Ignis commit.
    """
    try:
        from ignis.__commit__ import __commit_msg__  # type: ignore

        return __commit_msg__
    except (ImportError, ValueError):
        return ""
