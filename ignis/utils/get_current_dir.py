import os
import inspect

def get_current_dir() -> str:
    """
    Returns the directory of the Python file where this function is called.
    """
    frame = inspect.stack()[1]
    caller_file = frame.filename
    return os.path.dirname(os.path.abspath(caller_file))
