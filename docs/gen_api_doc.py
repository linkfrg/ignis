#!/usr/bin/env python3
"""Script for generating API docs for Widgets and Utils"""

import os
import sys
import inspect


sys.path.insert(0, os.path.abspath(".."))

from ignis.widgets import Widget  # noqa: E402
from ignis.utils import Utils  # noqa: E402

API_REFERENCE_DIR = "api_reference"


def format_service_name(name: str) -> str:
    result = []
    words = name.split("_")
    for i in words:
        result.append(i.capitalize())

    return " ".join(result)


def format_widget_template(name: str) -> None:
    return f"""{name}
{'-'*len(name)}

.. autoclass:: ignis.widgets.Widget.{name}
    :members:
"""


def format_utils_function_template(name: str) -> None:
    return f"""{name}
{'-'*len(name)}

.. autofunction:: ignis.utils.Utils.{name}
"""


def format_utils_class_template(name: str) -> None:
    return f"""{name}
{'-'*len(name)}

.. autoclass:: ignis.utils.{name}
    :members:
"""


def clean(dir_name: str) -> None:
    files_to_keep = ["index.rst"]
    for filename in os.listdir(f"{API_REFERENCE_DIR}/{dir_name}"):
        file_path = os.path.join(dir_name, filename)
        if os.path.isfile(file_path) and filename not in files_to_keep:
            os.remove(file_path)


def _generate(klass: object, dir_name: str, transform: callable) -> None:
    for name in klass.__dict__:
        if name.startswith("__"):
            continue

        override_path = f"{API_REFERENCE_DIR}/{dir_name}/overrides/{name}"
        if os.path.exists(override_path):
            with open(override_path) as file:
                data = file.read()
        else:
            data = transform(name)

        with open(f"{API_REFERENCE_DIR}/{dir_name}/{name}.rst", "w") as file:
            file.write(data)


def generate_widgets() -> None:
    _generate(Widget, "widgets", format_widget_template)


def generate_utils() -> None:
    def check(name: str) -> str:
        if inspect.isclass(name):
            return format_utils_class_template(name)
        else:
            return format_utils_function_template(name)

    _generate(Utils, "utils", check)


def main() -> None:
    clean("widgets")
    clean("utils")
    generate_widgets()
    generate_utils()


if __name__ == "__main__":
    main()
