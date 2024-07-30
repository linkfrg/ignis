import os

VERSION_FILE = f"{os.path.dirname(os.path.abspath(__file__))}/../VERSION"

def get_ignis_version() -> str:
    """
    Get the current Ignis version.

    Returns:
        ``str``: The Ignis version.
    """
    with open(VERSION_FILE) as file:
        version = file.read()

    return version
