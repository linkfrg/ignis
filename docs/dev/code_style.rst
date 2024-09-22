Code Style Guidelines
========================

Code Formatting
-------------------

All code should be formmated using `Ruff, the Python code formatter <https://github.com/astral-sh/ruff>`_.

Definitions and Naming
-----------------------

Use specific naming conventions for different purposes:

- ``snake_case``: Functions, variables, GObject properties (except D-Bus methods/properties)
- ``SCREAMING_SNAKE_CASE``: Constants
- ``PascalCase``: Classes, D-Bus methods/properties
- ``kebab-case``: GObject signals