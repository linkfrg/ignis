import subprocess
from gi.repository import Gio  # type: ignore
from typing import Callable


def exec_sh(command: str) -> subprocess.CompletedProcess:
    """
    Execute a shell (bash) command.

    Args:
        command: The command to execute.

    Returns:
        The result of the command execution. You can use the ``stdout`` property to get the command's output.
    """
    return subprocess.run(command, shell=True, text=True, capture_output=True)


class AsyncCompletedProcess:
    """
    Completed process object for :func:`~ignis.utils.Utils.exec_sh_async`.
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
        """
        The return code of the process.
        """
        return self._returncode

    @property
    def stdout(self) -> str | None:
        """
        The output of the process.
        """
        return self._stdout

    @property
    def stderr(self) -> str | None:
        """
        The stderr (errors) of the process.
        """
        return self._stderr


def exec_sh_async(command: str, on_finished: Callable | None = None) -> Gio.Subprocess:
    """
    Execute a shell (bash) command asynchronously.

    Args:
        command: The command to execute.
        on_finished: A function to call when the process is finished. An instance of :class:`~ignis.utils.exec_sh.AsyncCompletedProcess` will be passed to this function.

    Returns:
        The instance of ``Gio.Subprocess``.
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
