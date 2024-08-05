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

Make a symbolic link to Ignis sources
-------------------------------------

Replace ``python3.12`` with actual version of python.

.. code-block:: bash
    
    rm -R venv/lib/python3.12/site-packages/ignis
    ln -sf $(pwd)/ignis venv/lib/python3.12/site-packages/ignis

Running Ignis
-------------

.. code-block:: bash

    ignis init
    