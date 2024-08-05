import os
import sys
import shutil
import inspect
from importlib.machinery import SourceFileLoader


def find_bin_directory():
    # Check if in a virtual environment
    if sys.base_prefix != sys.prefix:
        return os.path.join(sys.prefix, 'bin')

    # Check common system-wide bin directories
    common_bin_dirs = ['/bin', '/usr/bin']
    for bin_dir in common_bin_dirs:
        if os.path.isdir(bin_dir):
            return bin_dir

def find_script(filename: str) -> str:
    bin_dir = find_bin_directory()
    if not bin_dir:
        return

    script_path = os.path.join(bin_dir, filename)
    if os.path.isfile(script_path) and os.access(script_path, os.X_OK):
        return script_path

def import_script(name: str) -> None:
    script_path = find_script(name)
    if not script_path:
        raise ImportError(f"{name} executable not found in the bin directory.")

    SourceFileLoader(name, script_path).load_module()
    del sys.modules[name]

import_script("ignis")

sys.path.insert(0, os.path.abspath(".."))
from ignis.widgets import Widget  # noqa: E402
from ignis.utils import Utils  # noqa: E402

project = "Ignis"
copyright = "2024, linkfrg"
author = "linkfrg"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


html_theme = "sphinx_book_theme"
html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
]

html_title = "Ignis Wiki"
smartquotes = False

add_module_names = False


def get_widget_template(name: str) -> None:
    return f"""{name}
{'-'*len(name)}

.. autoclass:: ignis.widgets.Widget.{name}
"""


def get_service_template(name: str) -> None:
    return f"""{name.capitalize().replace("_", "")}
{'-'*len(name)}

.. automodule:: ignis.services.{name}
    :members:
"""


def get_utils_function_template(name: str) -> None:
    return f"""{name}
{'-'*len(name)}

.. autofunction:: ignis.utils.Utils.{name}
"""


def get_utils_class_template(name: str) -> None:
    return f"""{name}
{'-'*len(name)}

.. autoclass:: ignis.utils.{name}
    :members:
"""

for i in ["widgets", "services", "utils"]:
    try:
        shutil.rmtree(f"{i}/generated")
    except FileNotFoundError:
        pass
    os.makedirs(f"{i}/generated", exist_ok=True)

for name in Widget.__dict__:
    if name.startswith("__"):
        continue

    override_path = f"widgets/overrides/{name}"
    if os.path.exists(override_path):
        with open(override_path) as file:
            data = file.read()
    else:
        data = get_widget_template(name)

    with open(f"widgets/generated/{name}.rst", "w") as file:
        file.write(data)

for filename in os.listdir("../ignis/services"):
    if filename.startswith("__"):
        continue

    name = filename.replace(".py", "")
    with open(f"services/generated/{name}.rst", "w") as file:
        file.write(get_service_template(name))

for name in Utils.__dict__:
    if name.startswith("__"):
        continue

    override_path = f"utils/overrides/{name}"
    if os.path.exists(override_path):
        with open(override_path) as file:
            data = file.read()
    else:
        if inspect.isclass(name):
            data = get_utils_class_template(name)
        else:
            data = get_utils_function_template(name)


    with open(f"utils/generated/{name}.rst", "w") as file:
        file.write(data)
