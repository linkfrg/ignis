import os
import click
import collections
from ignis.client import IgnisClient
from ignis.utils import Utils
from ignis.exceptions import WindowNotFoundError
from typing import Any

DEFAULT_CONFIG_PATH = "~/.config/ignis/config.py"


class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super().__init__(name, commands, **attrs)
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands


def get_version_message() -> str:
    return f"""Ignis {Utils.get_ignis_version()}
Branch: {Utils.get_ignis_branch()}
Commit: {Utils.get_ignis_commit()} ({Utils.get_ignis_commit_msg()})"""


def get_systeminfo() -> str:
    current_desktop = os.getenv("XDG_CURRENT_DESKTOP")
    with open("/etc/os-release") as file:
        os_release = file.read().strip()

    return f"""{get_version_message()}
Current desktop: {current_desktop}

os-release:
{os_release}"""


def print_version(ctx, param, value):
    if value:
        ctx.exit(print(get_version_message()))


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


@click.group(cls=OrderedGroup)
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Print version and exit",
)
def cli():
    pass


@cli.command(name="init", help="Initialize Ignis")
@click.option(
    "--config",
    "-c",
    help=f"Path to the configuration file (default: {DEFAULT_CONFIG_PATH})",
    default=DEFAULT_CONFIG_PATH,
    type=str,
    metavar="PATH",
)
@click.option("--debug", help="Print debug information to terminal", is_flag=True)
def init(config: str, debug: bool) -> None:
    from ignis.app import run_app

    client = IgnisClient()

    if client.has_owner:
        print("Ignis is already running")
        exit(1)

    config_path = os.path.expanduser(config)
    run_app(config_path, debug)


@cli.command(name="open", help="Open window")
@click.argument("window")
def open_window(window: str) -> None:
    call_client_func("open_window", window)


@cli.command(name="close", help="Close window")
@click.argument("window")
def close(window: str) -> None:
    call_client_func("close_window", window)


@cli.command(name="toggle", help="Toggle window")
@click.argument("window")
def toggle(window: str) -> None:
    call_client_func("toggle_window", window)


@cli.command(name="list-windows", help="List all windows")
def list_windows() -> None:
    window_list = call_client_func("list_windows")
    print("\n".join(window_list))


@cli.command(name="run-python", help="Execute python code")
@click.argument("code")
def run_python(code: str) -> None:
    call_client_func("run_python", code)


@cli.command(name="run-file", help="Execute python file")
@click.argument("file")
def run_file(file: str) -> None:
    call_client_func("run_file", file)


@cli.command(name="inspector", help="Open GTK Inspector")
def inspector() -> None:
    call_client_func("inspector")


@cli.command(name="reload", help="Reload Ignis")
def reload() -> None:
    call_client_func("reload")


@cli.command(name="quit", help="Quit Ignis")
def quit() -> None:
    call_client_func("quit")


@cli.command(name="systeminfo", help="Print system information")
def systeminfo() -> None:
    print(get_systeminfo())
