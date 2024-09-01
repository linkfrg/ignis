import subprocess
from gi.repository import Gio  # type: ignore
from typing import Callable, Optional


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
        - **returncode** (``int``, not argument, read-only): The return code of the process.
        - **stdout** (``str | None``, not argument, read-only): The output of the process.
        - **stderr** (``str | None``, not argument, read-only): The errors of the process.
    """

    def __init__(self, process: Gio.Subprocess) -> None:
        self._returncode: int = -1
        self._stdout: str | None = None
        self._stderr: str | None = None

        data = process.communicate(None, None)
        if data[0]:
            self._returncode = process.get_exit_status()
            stdout_bytes = data[1].get_data()
            stderr_bytes = data[2].get_data()

            if stdout_bytes:
                self._stdout = stdout_bytes.decode()
            if stderr_bytes:
                self._stderr = stderr_bytes.decode()

    @property
    def returncode(self) -> int:
        return self._returncode

    @property
    def stdout(self) -> str | None:
        return self._stdout

    @property
    def stderr(self) -> str | None:
        return self._stderr


def exec_sh_async(
    command: str, on_finished: Optional[Callable] = None
) -> Gio.Subprocess:
    """
    Execute a shell (bash) command asynchronously.

    Args:
        command (``str``): The command to execute.
        on_finished (``Callable``, optional): A function to call when the process is finished. An instance of :class:`~ignis.utils.exec_sh.AsyncCompletedProcess` will be passed to this function.

    Returns:
        ``Gio.Subprocess``
    """

    def wait_check_callback(process: Gio.Subprocess, result: Gio.AsyncResult) -> None:
        process.wait_check_finish(result)
        on_finished(AsyncCompletedProcess(process))  # type: ignore

    process = Gio.Subprocess.new(
        ["bash", "-c", command],
        Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
    )
    if on_finished:
        process.wait_check_async(None, wait_check_callback)

    return process
