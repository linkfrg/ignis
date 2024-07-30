import os
import sys
import shutil

sys.path.insert(0, os.path.abspath(".."))
from ignis.widgets import Widget

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


def get_widget_template(name):
    return f"""{name}
{'-'*len(name)}

.. autoclass:: ignis.widgets.Widget.{name}
"""


def get_service_template(name):
    return f"""{name.capitalize().replace("_", "")}
{'-'*len(name)}

.. automodule:: ignis.services.{name}
    :members:
"""


def get_utils_function_template(name):
    return f"""{name}
{'-'*len(name)}

.. autofunction:: ignis.utils.Utils.{name}
"""


def get_utils_class_template(name):
    return f"""{name}
{'-'*len(name)}

.. automodule:: ignis.utils.{name}
    :members:
"""


for i in ["widgets", "services", "utils"]:
    try:
        shutil.rmtree(f"{i}/generated")
    except FileNotFoundError:
        pass
    os.makedirs(f"{i}/generated", exist_ok=True)

for name in Widget.__dict__:
    if not name.startswith("__"):
        with open(f"widgets/generated/{name}.rst", "w") as file:
            file.write(get_widget_template(name))

for filename in os.listdir("../ignis/services"):
    if not filename.startswith("__"):
        name = filename.replace(".py", "")
        with open(f"services/generated/{name}.rst", "w") as file:
            file.write(get_service_template(name))

for filename in os.listdir("../ignis/utils"):
    if not filename.startswith("__"):
        name = filename.replace(".py", "")
        with open(f"utils/generated/{name}.rst", "w") as file:
            file.write(get_utils_class_template(name))
