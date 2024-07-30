import os
import click
import ctypes
import collections
from ignis.client import IgnisClient
from ignis.utils import Utils

DEFAULT_CONFIG_PATH = "~/.config/ignis/config.py"


class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super().__init__(name, commands, **attrs)
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands


def set_process_name(name):
    libc = ctypes.CDLL("libc.so.6")
    libc.prctl(15, ctypes.c_char_p(name.encode()), 0, 0, 0)


def print_version(ctx, param, value):
    if value:
        ctx.exit(print(f"Ignis {Utils.get_ignis_version()}"))


def call_client_func(name: str, *args) -> None:
    client = IgnisClient()
    if not client.has_owner:
        print("Ignis is not running.")
        exit(1)
    getattr(client, name)(*args)


@click.group(cls=OrderedGroup)
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Print version and exit",
)
def main():
    set_process_name("ignis")


@main.command(name="init", help="Initialize Ignis")
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
    client = IgnisClient()
    if client.has_owner:
        print("Ignis is already running")
        exit(1)
    run_server(config)


@main.command(name="open", help="Open window")
@click.argument("window")
def open(window: str) -> None:
    call_client_func("OpenWindow", window)


@main.command(name="close", help="Close window")
@click.argument("window")
def close(window: str) -> None:
    call_client_func("CloseWindow", window)


@main.command(name="toggle", help="Toggle window")
@click.argument("window")
def toggle(window: str) -> None:
    call_client_func("ToggleWindow", window)


@main.command(name="list-windows", help="List all windows")
def list_windows() -> None:
    call_client_func("ListWindows")


@main.command(name="run-python", help="Execute inline python code")
@click.argument("code")
def run_python(code: str) -> None:
    call_client_func("RunPython", code)


@main.command(name="run-file", help="Execute python file")
@click.argument("file")
def run_file(file: str) -> None:
    call_client_func("RunFile", file)


@main.command(name="inspector", help="Open GTK Inspector")
def inspector() -> None:
    call_client_func("Inspector")


@main.command(name="reload", help="Reload Ignis")
def reload() -> None:
    call_client_func("Reload")


@main.command(name="quit", help="Quit Ignis")
def quit() -> None:
    call_client_func("Quit")


def run_server(config: str) -> None:
    from ignis.app import app

    config_path = os.path.expanduser(config)
    app._setup(config_path)

    try:
        app.run(None)
    except KeyboardInterrupt:
        pass  # app.quit() will be called automatically


if __name__ == "__main__":
    main()
