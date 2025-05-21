import os
import typer
import subprocess
from ignis.client import IgnisClient
from ignis.utils import Utils
from ignis.exceptions import WindowNotFoundError
from typing import Any
from ignis import is_editable_install, is_sphinx_build
from typing import Annotated

# Do not import gi.repository during sphinx build
# Otherwise, ignis.cli package will be unavailable:
# ``AttributeError: module 'ignis' has no attribute 'cli' [docutils]``
if is_sphinx_build:
    DEFAULT_CONFIG_PATH = ""  # not used during sphinx build, just set to empty string
else:
    from gi.repository import GLib  # type: ignore

    DEFAULT_CONFIG_PATH = f"{GLib.get_user_config_dir()}/ignis/config.py"


cli_app = typer.Typer(
    name="ignis",
    help="A widget framework for building desktop shells, written and configurable in Python.",
    no_args_is_help=True,
)


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


def get_version_message() -> str:
    if not is_editable_install:
        return f"""Ignis {Utils.get_ignis_version()}
Branch: {Utils.get_ignis_branch()}
Commit: {Utils.get_ignis_commit()} ({Utils.get_ignis_commit_msg()})"""
    else:
        commit = _run_git_cmd("rev-parse HEAD")
        branch = _run_git_cmd("branch --show-current")
        commit_msg = _run_git_cmd("log -1 --pretty=%B")
        return f"""Ignis {Utils.get_ignis_version()}
Editable install
Branch: {branch}
Commit: {commit} ({commit_msg})

Version at the moment of the installation:
Branch: {Utils.get_ignis_branch()}
Commit: {Utils.get_ignis_commit()} ({Utils.get_ignis_commit_msg()})
"""


def get_systeminfo() -> str:
    current_desktop = os.getenv("XDG_CURRENT_DESKTOP")
    with open("/etc/os-release") as file:
        os_release = file.read().strip()

    return f"""{get_version_message()}
Current desktop: {current_desktop}

os-release:
{os_release}"""


def call_client_func(name: str, *args) -> Any:
    client = IgnisClient()
    if not client.has_owner:
        print("Ignis is not running")
        exit(1)

    try:
        return getattr(client, name)(*args)
    except WindowNotFoundError:
        print(f"No such window: {args[0]}")
        exit(1)


def get_full_path(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


def version_callback(value: bool):
    if value:
        typer.echo(get_version_message())
        raise typer.Exit()


@cli_app.callback()
def main_callback(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Print version and exit.",
        ),
    ] = None,
):
    return


@cli_app.command()
def init(
    config: Annotated[
        str,
        typer.Option(
            help="Path to the configuration file.",
            metavar="PATH",
            show_default="~/.config/ignis/config.py",
        ),
    ] = DEFAULT_CONFIG_PATH,
    debug: Annotated[
        bool, typer.Option(help="Print debug information to terminal.")
    ] = False,
) -> None:
    """
    Initialize Ignis.
    """
    from ignis.app import run_app

    client = IgnisClient()

    if client.has_owner:
        print("Ignis is already running")
        exit(1)

    config_path = get_full_path(config)
    run_app(config_path, debug)


WindowArgument = Annotated[
    str,
    typer.Argument(
        help="The name of the window.", metavar="WINDOW_NAME", show_default=False
    ),
]


@cli_app.command()
def open_window(window: WindowArgument) -> None:
    """
    Open a window.
    """
    call_client_func("open_window", window)


@cli_app.command()
def close_window(window: WindowArgument) -> None:
    """
    Close a window.
    """
    call_client_func("close_window", window)


@cli_app.command()
def toggle_window(window: WindowArgument) -> None:
    """
    Toggle a window.
    """
    call_client_func("open_window", window)


@cli_app.command()
def list_windows() -> None:
    """
    List names of all windows.
    """
    window_list = call_client_func("list_windows")
    print("\n".join(window_list))


@cli_app.command()
def run_python(
    code: Annotated[
        str,
        typer.Argument(help="The code to execute.", metavar="CODE", show_default=False),
    ],
) -> None:
    """
    Execute a Python code inside the running Ignis process.
    """
    call_client_func("run_python", code)


@cli_app.command()
def run_file(
    file: Annotated[
        str,
        typer.Argument(help="The file to execute.", metavar="PATH", show_default=False),
    ],
) -> None:
    """
    Execute a Python file inside the running Ignis process.
    """
    call_client_func("run_file", get_full_path(file))


@cli_app.command()
def inspector() -> None:
    """
    Open GTK Inspector.
    """
    call_client_func("inspector")


@cli_app.command()
def reload() -> None:
    """
    Reload Ignis.
    """
    call_client_func("reload")


@cli_app.command()
def quit() -> None:
    """
    Quit Ignis.
    """
    call_client_func("quit")


@cli_app.command()
def systeminfo() -> None:
    """
    Print system information.
    """
    print(get_systeminfo())
