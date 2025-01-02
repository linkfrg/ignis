Setting up a Development Environment
=====================================

Firstly, clone the repository:

.. code-block:: bash

    # replace with the actual URL of your fork (if needed)
    git clone https://github.com/linkfrg/ignis.git
    cd ignis

Then, run the script:

.. code-block:: bash
    
    bash tools/setup_devenv.sh

It will create a Python virtual environment, 
install Ignis with its dependencies (including dev dependencies), and create a symbolic link to the Ignis source files.

Now you can edit the ``ignis`` directory at the root of the repository, 
and the changes will be applied without the need to reinstall Ignis.
