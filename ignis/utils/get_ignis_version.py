import os
import subprocess
from ignis import __version__


def get_ignis_version() -> str:
    """
    Get the current Ignis version.

    Returns:
        ``str``: The Ignis version.
    """
    return __version__


def _get_commit_hash():
    try:
        repo_dir = os.path.abspath(os.path.join(__file__, "../.."))
        commit_hash = subprocess.run(
            f"git -C {repo_dir} rev-parse HEAD",
            shell=True,
            text=True,
            capture_output=True,
        ).stdout.strip()

        return commit_hash
    except subprocess.CalledProcessError:
        return None


def get_ignis_commit() -> str:
    """
    Get the current Ignis commit hash.

    Returns:
        ``str``: The Ignis commit hash.
    """

    try:
        from ignis.__commit__ import __commit__  # type: ignore
    except (ImportError, ValueError):
        __commit__ = _get_commit_hash()

    return __commit__
