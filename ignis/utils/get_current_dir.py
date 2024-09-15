import os


def get_current_dir() -> str:
    """
    Returns the path of the directory containing the current Python file.
    """
    return os.path.dirname(os.path.abspath(__file__))
