import os
import sys
import inspect
from typing import Callable
from sphinx.ext.autodoc.mock import mock

sys.path.insert(0, os.path.abspath(".."))

project = "Ignis"
copyright = "2024, linkfrg"
author = "linkfrg"
REPO_URL = "https://github.com/linkfrg/ignis"
DOCS_URL = "https://linkfrg.github.io/ignis/latest"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_design",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


autodoc_mock_imports = ["gi", "loguru", "setuptools", "click", "cairo", "requests"]
autodoc_member_order = "bysource"

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

html_css_files = ["css/custom.css"]

html_title = "Ignis documentation"

smartquotes = False
add_module_names = False

json_url = f"{DOCS_URL}/_static/switcher.json"

version_match = os.getenv("DOCS_VERSION")

if not version_match or version_match == "latest":
    version_match = "dev"

release = version_match

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
    "navbar_align": "left",
    "navbar_center": ["version-switcher", "navbar-nav"],
    "secondary_sidebar_items": {
        "**/*": ["page-toc", "edit-this-page", "sourcelink"],
    },
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

API_REFERENCE_DIR = "api"


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


def _generate(klass: object, dir_name: str, transform: Callable) -> None:
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


def generate_widgets(klass) -> None:
    _generate(klass, "widgets", format_widget_template)


def generate_utils(klass) -> None:
    def check(name: str) -> str:
        if inspect.isclass(name):
            return format_utils_class_template(name)
        else:
            return format_utils_function_template(name)

    _generate(klass, "utils", check)

with mock(autodoc_mock_imports):
    from ignis.widgets import Widget
    from ignis.utils import Utils
    clean("widgets")
    clean("utils")
    generate_widgets(Widget)
    generate_utils(Utils)
