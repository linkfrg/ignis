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

Pip
----

Pip is the standard package manager for Python.  
You can install Ignis directly from the Git repository using Pip.

.. hint::
    
    You can do this in a Python virtual environment.
    Create and activate one with the following commands:
    
    .. code-block:: bash

        python -m venv venv
        source venv/bin/activate  # for fish: . venv/bin/activate.fish

To install the latest (Git) version of Ignis:

.. code-block:: bash

    pip install git+https://github.com/linkfrg/ignis.git

To install a specific version (e.g., ``v0.5``):

.. code-block:: bash

    # replace "TAG" with the desired Git tag
    pip install git+https://github.com/linkfrg/ignis.git@TAG

.. seealso::

    For advanced usage, you can `set up a development environment <../dev/env.html>`_ and install Ignis in editable mode.
    This allows you to easily switch between commits, versions, branches, or pull requests using `git`, without having to reinstall Ignis.

Building from source
---------------------

**Dependencies:**

- ninja
- meson
- gtk4 
- gtk4-layer-shell
- glib-mkenums (glib2-devel)
- pygobject >= 3.50.0
- pycairo
- python-click
- python-loguru
- libpulse (if using PipeWire, install ``pipewire-pulse``)

.. code-block:: bash
    
    git clone https://github.com/linkfrg/ignis.git
    cd ignis
    meson setup build --prefix=/usr
    meson compile -C build
    meson install -C build


Running
--------

.. code-block:: bash

    ignis init
