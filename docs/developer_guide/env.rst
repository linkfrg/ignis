Setting up a Development Environment
=====================================

Clone repository
-------------------

.. code-block:: bash

    git clone https://github.com/linkfrg/ignis.git
    cd ignis

Create Python Virtual Environment
----------------------------------

.. code-block:: bash

    python -m venv venv

Activate Virtual Environment
----------------------------

- For Bash:

.. code-block:: bash

    source venv/bin/activate

- For Fish:

.. code-block:: fish

    . venv/bin/activate.fish

Install dependencies to Virtual Environment
-------------------------------------------

.. code-block:: bash

    pip install --upgrade -r requirements.txt

Additionally, install dependencies required by dotfiles/configuration.

Build and Install Ignis to Virtual Environment
----------------------------------------------

.. code-block:: bash

    meson setup build --prefix=$(pwd)/venv --libdir "lib/ignis"
    meson compile -C build
    meson install -C build

Copy ``__lib_dir__.py`` to Ignis sources
-------------------------------------------

.. code-blocK:: bash

    SITE_PACKAGES=$(python3 -c 'import site; print(site.getsitepackages()[0])')
    # for fish use this: 
    # set SITE_PACKAGES $(python3 -c 'import site; print(site.getsitepackages()[0])')

    cp $SITE_PACKAGES/ignis/__lib_dir__.py $(pwd)/ignis

Make a symbolic link to Ignis sources
-------------------------------------

.. code-block:: bash
    
    rm -R $SITE_PACKAGES/ignis
    ln -sf $(pwd)/ignis $SITE_PACKAGES/ignis

Running Ignis
-------------

.. code-block:: bash

    ignis init
    