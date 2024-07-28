#!/usr/bin/env python3

import compileall
import sys

install_dir = sys.argv[1]

compileall.compile_dir(install_dir, force=True, quiet=1)

