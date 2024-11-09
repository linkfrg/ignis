import os
import sys
import shutil

sys.path.insert(0, os.path.abspath("tmp"))

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
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
suppress_warnings = ["config.cache"]

autodoc_mock_imports = ["gi", "loguru", "setuptools", "click", "cairo", "requests"]
autodoc_member_order = "bysource"

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

html_css_files = ["css/custom.css"]

html_title = "Ignis documentation"

smartquotes = False
napoleon_use_param = True
typehints_use_signature = True
typehints_use_signature_return = True
typehints_defaults = "comma"

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
    "pygments_light_style": "tango",
    "pygments_dark_style": "monokai",
}


html_context = {
    "github_user": "linkfrg",
    "github_repo": "ignis",
    "github_version": "main",
    "doc_path": "docs/",
}


def copy_and_replace_gobject_property(source_dir: str, target_dir: str):
    """
    This trash function copys source_dir to target_dir
    and replaces @GObject.Property with @property.
    For what? To indicate Sphinx that GObject.Property functions is actually properties.
    """
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    shutil.copytree(source_dir, target_dir)

    for dirpath, _, filenames in os.walk(target_dir):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path) as file:
                    content = file.read()

                new_content = content.replace("@GObject.Property", "@property")

                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(new_content)


copy_and_replace_gobject_property("../ignis", "tmp/ignis")

API_REFERENCE_DIR = "api"
