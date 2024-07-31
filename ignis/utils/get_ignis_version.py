import os

VERSION_FILE = f"{os.path.dirname(os.path.abspath(__file__))}/../VERSION"


def get_ignis_version() -> str:
    """
    Get the current Ignis version and commit hash.

    Returns:
        ``str``: A string containing the Ignis version and commit hash.
    """
    with open(VERSION_FILE) as file:
        version = file.read()

    return version
