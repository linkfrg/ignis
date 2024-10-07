Installation
============

Arch linux
-----------

.. code-block:: bash

    paru -S ignis

Nix
----

Add Ignis to your flake's inputs:

.. code-block:: nix
    
    ignis.url = "github:linkfrg/ignis";

Then add the following to ``environment.systemPackages`` or ``home.packages``:

.. code-block:: nix
  
    inputs.ignis.packages.${system}.ignis

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


Running
--------

.. code-block:: bash

    ignis init