import os
import shutil
import subprocess
from ignis.exceptions import SassCompilationError, SassNotFoundError

TEMP_DIR = "/tmp/ignis"
COMPILED_CSS = f"{TEMP_DIR}/compiled.css"
os.makedirs(TEMP_DIR, exist_ok=True)

# pick a Sass compiler
sass_compiler = None

sass_compilers = [
    "sass", # dart-sass
    "grass" # grass-sass
]

for compiler in sass_compilers:
    sass_compiler = shutil.which(compiler)

    if sass_compiler:
        break


def compile_file(path: str) -> str:
    assert sass_compiler

    result = subprocess.run([sass_compiler, path, COMPILED_CSS], capture_output=True)

    if result.returncode != 0:
        raise SassCompilationError(result.stderr.decode())

    with open(COMPILED_CSS) as file:
        return file.read()


def compile_string(string: str) -> str:
    assert sass_compiler

    process = subprocess.Popen(
        [sass_compiler, "--stdin"],
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
    Requires either `Dart Sass <https://sass-lang.com/dart-sass/>`_
    or `Grass <https://github.com/connorskees/grass>`_.

    Args:
        path: The path to the SASS/SCSS file.
        string: A string with SASS/SCSS style.

    Raises:
        TypeError: If neither of the arguments is provided.
        SassNotFoundError: If no Sass compiler is available.
        SassCompilationError: If an error occurred while compiling SASS/SCSS.
    """
    if not sass_compiler:
        raise SassNotFoundError()

    if string:
        return compile_string(string)

    elif path:
        return compile_file(path)

    else:
        raise TypeError("sass_compile() requires at least one positional argument")
