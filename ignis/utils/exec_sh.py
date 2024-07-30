import subprocess
from gi.repository import Gio


def exec_sh(command: str) -> subprocess.CompletedProcess:
    """
    Execute a shell (bash) command.

    Args:
        command (``str``): The command to execute.

    Returns:
        ``subprocess.CompletedProcess``: The result of the command execution. You can use the ``stdout`` property to get the command's output.
    """
    return subprocess.run(command, shell=True, text=True, capture_output=True)


class AsyncCompletedProcess:
    """
    Completed process object for :func:`~ignis.utils.exec_sh.exec_sh_async`.

    Properties:
        - **returncode** (``int``, read-only): The return code of the process.
        - **stdout** (``str``, read-only): The output of the process.
        - **stderr** (``str``, read-only): The errors of the process.
    """

    def __init__(self, process: Gio.Subprocess) -> None:
        data = process.communicate(None, None)
        self._returncode = process.get_exit_status()
        self._stdout = data[1].get_data().decode()
        self._stderr = data[2].get_data().decode()
        print(self._stderr)

    @property
    def returncode(self) -> int:
        return self._returncode

    @property
    def stdout(self) -> str:
        return self._stdout

    @property
    def stderr(self) -> str:
        return self._stderr


def exec_sh_async(command: str, on_finished: callable = None) -> None:
    """
    Execute a shell (bash) command asynchronously.

    Args:
        command (``str``): The command to execute.
        on_finished (``callable``, optional): A function to call when the process is finished. An instance of :class:`~ignis.utils.exec_sh.AsyncCompletedProcess` will be passed to this function.

    """

    def wait_check_callback(process: Gio.Subprocess, result: Gio.AsyncResult) -> None:
        process.wait_check_finish(result)
        on_finished(AsyncCompletedProcess(process))

    process = Gio.Subprocess.new(
        ["bash", "-c", command],
        Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
    )
    if on_finished:
        process.wait_check_async(None, wait_check_callback)
    return process
