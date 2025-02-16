import subprocess
from gi.repository import Gio  # type: ignore


def exec_sh(command: str, **kwargs) -> subprocess.CompletedProcess:
    """
    Execute a shell (bash) command.

    Args:
        command: The command to execute.

    ``**kwargs`` will be passed to ``subprocess.run()``.

    Returns:
        The result of the command execution. You can use the ``stdout`` property to get the command's output.
    """
    return subprocess.run(command, shell=True, text=True, capture_output=True, **kwargs)


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


async def exec_sh_async(command: str) -> AsyncCompletedProcess:
    """
    Execute a shell (bash) command asynchronously.

    Args:
        command: The command to execute.
        on_finished: A function to call when the process is finished. An instance of :class:`~ignis.utils.exec_sh.AsyncCompletedProcess` will be passed to this function.

    Returns:
        The instance of ``Gio.Subprocess``.
    """

    process = Gio.Subprocess.new(
        ["bash", "-c", command],
        Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
    )

    await process.wait_check_async()
    return AsyncCompletedProcess(process)
