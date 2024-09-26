Code Style Guidelines
========================

Code Formatting
-------------------

All code must be formatted using `Ruff <https://github.com/astral-sh/ruff>`_.

Type checking
-----------------

The use of type hints is encouraged, 
and all code must be checked using `mypy <https://mypy-lang.org/>`_.

Definitions and Naming
-----------------------

Use the following naming conventions for different purposes:

- ``snake_case``: Functions, variables, GObject properties (except D-Bus methods/properties)
- ``SCREAMING_SNAKE_CASE``: Constants
- ``PascalCase``: Classes, D-Bus methods/properties
- ``kebab-case``: GObject signals