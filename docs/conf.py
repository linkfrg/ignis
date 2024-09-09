import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "Ignis"
copyright = "2024, linkfrg"
author = "linkfrg"
REPO_URL = "https://github.com/linkfrg/ignis"
DOCS_URL = "https://linkfrg.github.io/ignis/latest"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

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
