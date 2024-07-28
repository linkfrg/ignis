import os
import ctypes
import argparse
from ignis.client import IgnisClient
from ignis.utils import Utils

DEFAULT_CONFIG_PATH = "~/.config/ignis/config.py"


def set_process_name(name):
    libc = ctypes.CDLL("libc.so.6")
    libc.prctl(15, ctypes.c_char_p(name.encode()), 0, 0, 0)


def parse_arguments():
    parser = argparse.ArgumentParser(description="", prog="ignis")
    parser.add_argument(
        "--config",
        "-c",
        default=DEFAULT_CONFIG_PATH,
        help=f"Path to the configuration file (default: {DEFAULT_CONFIG_PATH})",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print debug information to terminal",
    )
    parser.add_argument(
        "--open",
        metavar="WINDOW",
        help="Open a window",
    )
    parser.add_argument(
        "--close",
        metavar="WINDOW",
        help="Close a window",
    )
    parser.add_argument(
        "--toggle",
        metavar="WINDOW",
        help="Toggle a window",
    )
    parser.add_argument(
        "--list-windows",
        action="store_true",
        help="List all windows",
    )
    parser.add_argument(
        "--run-python",
        metavar="CODE",
        help="Execute inline python code",
    )
    parser.add_argument(
        "--run-file",
        metavar="FILE",
        help="Execute python file",
    )
    parser.add_argument(
        "--inspector",
        action="store_true",
        help="Open Inspector",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Reload ignis",
    )
    parser.add_argument(
        "--quit",
        action="store_true",
        help="Quit ignis",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print version",
    )

    return parser.parse_args()


def main():
    set_process_name("ignis")
    args = parse_arguments()
    client = IgnisClient()
    
    if not client.has_owner:
        run_server(args.config)
    else:
        if args.open:
            client.OpenWindow(args.open)

        elif args.close:
            client.CloseWindow(args.close)

        elif args.toggle:
            client.ToggleWindow(args.toggle)

        elif args.list_windows:
            client.ListWindows()

        elif args.run_python:
            client.RunPython(args.run_python)

        elif args.run_file:
            client.RunFile(args.run_file)

        elif args.inspector:
            client.Inspector()

        elif args.reload:
            client.Reload()

        elif args.quit:
            client.Quit()

        elif args.version:
            print(f"Ignis {Utils.get_ignis_version()}")
            
        else:
            print("Ignis is already running")
            exit(1)


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
