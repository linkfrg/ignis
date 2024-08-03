Installation
============

Arch linux
-----------

.. code-block:: bash

    paru -S ignis

Building from source
---------------------

**Dependencies:**

- git 
- ninja 
- meson 
- gtk4 
- gtk4-layer-shell
- pygobject
- pycairo
- python-click
- libpulse (if using PipeWire, install ``pipewire-pulse``)

.. code-block:: bash
    
    git clone https://github.com/linkfrg/ignis.git
    cd ignis
    meson setup build --prefix=/usr --libdir "lib/ignis"
    meson compile -C build
    meson install -C build


