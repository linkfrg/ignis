#!/bin/bash

meson subprojects download

python -m venv venv
source venv/bin/activate

pip install --upgrade -r requirements.txt
pip install --upgrade -r dev.txt

SITE_PACKAGES=$(python3 -c "import site; print(site.getsitepackages()[0])")

unlink $SITE_PACKAGES/ignis

meson setup build --prefix=$(pwd)/venv --libdir "lib/ignis"
meson compile -C build
meson install -C build

rm -R $SITE_PACKAGES/ignis
ln -sf $(pwd)/ignis $SITE_PACKAGES/ignis