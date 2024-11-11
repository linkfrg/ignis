import os
import subprocess
from ignis.exceptions import SassCompilationError, DartSassNotFoundError

TEMP_DIR = "/tmp/ignis"
COMPILED_CSS = f"{TEMP_DIR}/compiled.css"
os.makedirs(TEMP_DIR, exist_ok=True)


def compile_file(path: str) -> str:
    result = subprocess.run(["sass", path, COMPILED_CSS], capture_output=True)

    if result.returncode != 0:
        raise SassCompilationError(result.stderr.decode())

    with open(COMPILED_CSS) as file:
        return file.read()


def compile_string(string: str) -> str:
    process = subprocess.Popen(
        ["sass", "--stdin"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate(input=string.encode())

    if process.returncode != 0:
        raise SassCompilationError(stderr.decode())
    else:
        return stdout.decode()


def sass_compile(path: str | None = None, string: str | None = None) -> str:
    """
    Compile a SASS/SCSS file or string.
    Requires `Dart Sass <https://sass-lang.com/dart-sass/>`_.

    Args:
        path: The path to the SASS/SCSS file.
        string: A string with SASS/SCSS style.

    Raises:
        TypeError: If neither of the arguments is provided.
        DartSassNotFoundError: If Dart Sass not found.
        SassCompilationError: If an error occurred while compiling SASS/SCSS.
    """
    if not os.path.exists("/bin/sass"):
        raise DartSassNotFoundError()

    if string:
        return compile_string(string)

    elif path:
        return compile_file(path)

    else:
        raise TypeError("sass_compile() requires at least one positional argument")
