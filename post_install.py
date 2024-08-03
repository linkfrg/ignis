#!/usr/bin/env python3

import sys
import shutil
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
commit_hash_file = script_dir / "COMMIT"
ignis_version_file = Path(install_dir) / "VERSION"
ignis_commit_hash_file = Path(install_dir) / "COMMIT"

try:
    shutil.copy(version_file, ignis_version_file)
except shutil.SameFileError:
    pass

with open(commit_hash_file, "w") as file:
    file.write(commit_hash)

try:
    shutil.copy(commit_hash_file, ignis_commit_hash_file)
except shutil.SameFileError:
    pass
