import ctypes
from ignis.cli import cli


def set_process_name(name):
    libc = ctypes.CDLL("libc.so.6")
    libc.prctl(15, ctypes.c_char_p(name.encode()), 0, 0, 0)


def main():
    set_process_name("ignis")
    cli(prog_name="ignis")


if __name__ == "__main__":
    main()
