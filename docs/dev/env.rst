Setting up a Development Environment
=====================================

This guide with walk you through process of setting up a Development Environment for working on Ignis.

Source
------

Firstly, you have to grab the Ignis sources:

.. code-block:: bash

    # replace with the actual URL of your fork (if needed)
    git clone https://github.com/ignis-sh/ignis.git
    cd ignis

Virtual Environment
-------------------

It's always a good practice to work within a Python virtual environment.

.. code-block:: bash

    python -m venv venv
    source venv/bin/activate  # for fish: . venv/bin/activate.fish

Editable install
----------------

Ignis is build with Meson and meson-python. 
In order to support editable installs, Meson-python, Meson, and Ninja should be installed in the virtual environment.

.. code-block:: python

    pip install meson-python meson ninja

Now, install Ignis in the local virtual environment with the ``--no-build-isolation`` and ``-e`` options for an editable install.

.. code-block:: bash

    pip install --no-build-isolation -e .

Additionally, you can install useful development tools by running:

.. code-block:: bash

    pip install -r dev.txt

Done!

You can now edit the ``ignis`` directory at the root of the repository,
and the changes will be applied without the need to reinstall Ignis.
