import os
import shutil
import subprocess
import typing
from ignis.exceptions import SassCompilationError, SassNotFoundError

TEMP_DIR = "/tmp/ignis"
COMPILED_CSS = f"{TEMP_DIR}/compiled.css"
os.makedirs(TEMP_DIR, exist_ok=True)

# resolve Sass compiler paths and pick a default one
# "sass" (dart-sass) is the default,
# "grass" is an API-compatible drop-in replacement
known_compilers = typing.Literal["sass", "grass"]
sass_compilers = {}
for cmd in typing.get_args(known_compilers):
    path = shutil.which(cmd)
    if path:
        sass_compilers[cmd] = path
        

def compile_file(path: str, compiler_path: str) -> str:
    result = subprocess.run([compiler_path, path, COMPILED_CSS], capture_output=True)

    if result.returncode != 0:
        raise SassCompilationError(result.stderr.decode())

    with open(COMPILED_CSS) as file:
        return file.read()


def compile_string(string: str, compiler_path: str) -> str:
    process = subprocess.Popen(
        [compiler_path, "--stdin"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate(input=string.encode())

    if process.returncode != 0:
        raise SassCompilationError(stderr.decode())
    else:
        return stdout.decode()


def sass_compile(path: str | None = None, string: str | None = None, compiler: known_compilers | None = None) -> str:
    """
    Compile a SASS/SCSS file or string.
    Requires either `Dart Sass <https://sass-lang.com/dart-sass/>`_
    or `Grass <https://github.com/connorskees/grass>`_.

    Args:
        path: The path to the SASS/SCSS file.
        string: A string with SASS/SCSS style.
        compiler: The desired Sass compiler, either ``sass`` or ``grass``.

    Raises:
        TypeError: If neither of the arguments is provided.
        SassNotFoundError: If no Sass compiler is available.
        SassCompilationError: If an error occurred while compiling SASS/SCSS.
    """
    if not sass_compilers:
        raise SassNotFoundError()

    if compiler and compiler not in sass_compilers:
        raise SassNotFoundError()

    if compiler:
        compiler_path = sass_compilers[compiler]
    else:
        compiler_path = next(iter(sass_compilers.values()))

    if string:
        return compile_string(string, compiler_path)

    elif path:
        return compile_file(path, compiler_path)

    else:
        raise TypeError("sass_compile() requires at least one positional argument")
