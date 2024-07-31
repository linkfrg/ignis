#!/usr/bin/env python3

import sys
import subprocess
import compileall
from pathlib import Path

install_dir = sys.argv[1]

compileall.compile_dir(install_dir, force=True, quiet=1)

commit_hash = subprocess.run(
    "git rev-parse HEAD", shell=True, text=True, capture_output=True
).stdout.strip()

script_dir = Path(__file__).resolve().parent

version_file = script_dir / "VERSION"
with open(version_file) as file:
    version = file.read()

ignis_version_file = Path(install_dir) / "VERSION"
with open(ignis_version_file, "w") as file:
    file.write(f"{version} {commit_hash}")
