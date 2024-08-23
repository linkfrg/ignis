#!/usr/bin/bash

# install gtk4-layer-shell
git clone https://github.com/wmww/gtk4-layer-shell.git
cd gtk4-layer-shell
meson setup build --prefix=~/.local --libdir "lib"
ninja -C build
ninja -C build install

# build & install ignis
cd ..
PKG_CONFIG_PATH=~/.local/lib/pkgconfig meson setup build --prefix=$READTHEDOCS_VIRTUALENV_PATH --libdir "lib/ignis"
meson compile -C build
meson install -C build