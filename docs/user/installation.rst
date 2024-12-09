Installation
============

Arch Linux
-----------

maintainer: @linkfrg

Install the package from AUR.

.. code-block:: bash

    paru -S ignis

For the latest (git) version of Ignis install ``ignis-git``

.. code-block:: bash

    paru -S ignis-git

Nix
---

maintainer: missing specific maintainers, the package is mostly maintained by free contributors (bugs are expected)

Contributors:
    - @frdiener
    - @somokill
    - @ratson
    - @0x006E

.. warning::
    This will install the latest (git) version of Ignis.
    Please refer to the `latest documentation <https://linkfrg.github.io/ignis/latest/index.html>`_.

Add Ignis to your flake's inputs:

.. code-block:: nix
    
    ignis.url = "github:linkfrg/ignis";

Then add the following to ``environment.systemPackages`` or ``home.packages``:

.. code-block:: nix
  
    inputs.ignis.packages.${system}.ignis

Building from source
---------------------

**Dependencies:**

- ninja
- meson
- gtk4 
- gtk4-layer-shell
- glib-mkenums (glib2-devel)
- pygobject
- pycairo
- python-click
- python-loguru
- python-requests
- libpulse (if using PipeWire, install ``pipewire-pulse``)

.. code-block:: bash
    
    git clone https://github.com/linkfrg/ignis.git
    cd ignis
    meson setup build --prefix=/usr --libdir "lib/ignis"
    meson compile -C build
    meson install -C build


Running
--------

.. code-block:: bash

    ignis init
