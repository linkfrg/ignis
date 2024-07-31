import os

IGNIS_INSTALL_DIR = f"{os.path.dirname(os.path.abspath(__file__))}/.."

VERSION_FILE = f"{IGNIS_INSTALL_DIR}/VERSION"
COMMIT = f"{IGNIS_INSTALL_DIR}/COMMIT"


def get_ignis_version() -> str:
    """
    Get the current Ignis version.

    Returns:
        ``str``: The Ignis version.
    """
    with open(VERSION_FILE) as file:
        version = file.read()

    return version


def get_ignis_commit_hash() -> str:
    """
    Get the current Ignis commit hash.

    Returns:
        ``str``: The Ignis commit hash.
    """
    with open(COMMIT) as file:
        commit_hash = file.read()

    return commit_hash
