#!/usr/bin/env python3
"""Extract version number from __init__.py"""
import os

init_py = os.path.join(os.path.dirname(__file__), "../ignis/__init__.py")

data = open(init_py).readlines()
version_line = next(line for line in data if line.startswith("__version__ ="))

version = version_line.strip().split(" = ")[1].replace('"', "").replace("'", "")

print(version)
