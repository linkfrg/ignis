import gi
import os
import sys
import shutil
import inspect

gi.require_version("GIRepository", "2.0")
from gi.repository import GIRepository  # noqa: E402


def find_lib_dir():
    # Check if in a virtual environment
    if sys.base_prefix != sys.prefix:
        return os.path.join(sys.prefix, "lib", "ignis")

    # Check common system-wide bin directories
    common_lib_dirs = ["/lib/ignis", "/usr/lib/ignis"]
    for lib_dir in common_lib_dirs:
        if os.path.isdir(lib_dir):
            return lib_dir


lib_dir = find_lib_dir()
GIRepository.Repository.prepend_library_path(lib_dir)
GIRepository.Repository.prepend_search_path(lib_dir)

sys.path.insert(0, os.path.abspath(".."))

import ignis  # noqa: E402
from ignis.widgets import Widget  # noqa: E402
from ignis.utils import Utils  # noqa: E402

project = "Ignis"
copyright = "2024, linkfrg"
author = "linkfrg"
REPO_URL = "https://github.com/linkfrg/ignis"
DOCS_URL = "https://pyignis.readthedocs.io/en/latest"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

html_css_files = ["css/custom.css"]

html_title = "Ignis documentation"

smartquotes = False
add_module_names = False

json_url = f"{DOCS_URL}/_static/switcher.json"

version_match = os.environ.get("READTHEDOCS_VERSION")
release = ignis.__version__

version_match = f"v{release}"

html_theme_options = {
    "use_edit_page_button": True,
    "logo": {
        "text": "Ignis",
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": REPO_URL,
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        }
    ],
    "show_version_warning_banner": True,
    "switcher": {
        "json_url": json_url,
        "version_match": version_match,
    },
}

html_context = {
    "github_user": "linkfrg",
    "github_repo": "ignis",
    "github_version": "main",
    "doc_path": "docs/",
}


def format_service_name(name: str) -> str:
    result = []
    words = name.split("_")
    for i in words:
        result.append(i.capitalize())

    return " ".join(result)


def get_widget_template(name: str) -> None:
    return f"""{name}
{'-'*len(name)}

.. autoclass:: ignis.widgets.Widget.{name}
"""


def get_service_template(name: str) -> None:
    return f"""{format_service_name(name)}
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


API_REFERENCE_DIR = "api_reference"

for i in ["widgets", "services", "utils"]:
    try:
        shutil.rmtree(f"{API_REFERENCE_DIR}/{i}/generated")
    except FileNotFoundError:
        pass
    os.makedirs(f"{API_REFERENCE_DIR}/{i}/generated", exist_ok=True)

for name in Widget.__dict__:
    if name.startswith("__"):
        continue

    data = get_widget_template(name)
    with open(f"{API_REFERENCE_DIR}/widgets/generated/{name}.rst", "w") as file:
        file.write(data)

for filename in os.listdir("../ignis/services"):
    if filename.startswith("__"):
        continue

    name = filename.replace(".py", "")
    with open(f"{API_REFERENCE_DIR}/services/generated/{name}.rst", "w") as file:
        file.write(get_service_template(name))

for name in Utils.__dict__:
    if name.startswith("__"):
        continue

    override_path = f"{API_REFERENCE_DIR}/utils/overrides/{name}"
    if os.path.exists(override_path):
        with open(override_path) as file:
            data = file.read()
    else:
        if inspect.isclass(name):
            data = get_utils_class_template(name)
        else:
            data = get_utils_function_template(name)

    with open(f"{API_REFERENCE_DIR}/utils/generated/{name}.rst", "w") as file:
        file.write(data)
