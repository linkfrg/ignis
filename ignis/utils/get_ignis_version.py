import os
import subprocess
from ignis import __version__


def _run_git_cmd(args: str) -> str | None:
    try:
        repo_dir = os.path.abspath(os.path.join(__file__, "../.."))
        commit_hash = subprocess.run(
            f"git -C {repo_dir} {args}",
            shell=True,
            text=True,
            capture_output=True,
        ).stdout.strip()

        return commit_hash
    except subprocess.CalledProcessError:
        return None


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
    except (ImportError, ValueError):
        __commit__ = _run_git_cmd("rev-parse HEAD")

    return __commit__


def get_ignis_branch() -> str:
    """
    Get the name of the current Ignis git branch.

    Returns:
        The name of the Ignis git branch.
    """
    try:
        from ignis.__commit__ import __branch__  # type: ignore
    except (ImportError, ValueError):
        __branch__ = _run_git_cmd("branch --show-current")

    return __branch__


def get_ignis_commit_msg() -> str:
    """
    Get the message of the latest Ignis commit.

    Returns:
        The message of the latest Ignis commit.
    """
    try:
        from ignis.__commit__ import __commit_msg__  # type: ignore
    except (ImportError, ValueError):
        __commit_msg__ = _run_git_cmd("log -1 --pretty=%B")

    return __commit_msg__
