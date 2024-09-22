Documentation Guidelines
========================

Ignis uses the `Sphinx <https://www.sphinx-doc.org/en/master/>`_ documentation generator.
Additionally, Ignis uses the ``autodoc`` extension to generate documentation from Python docstrings.

.. hint::
    Sphinx uses the reStructuredText markup language.
    Here are some useful resources to learn more about it:

    - `reStructuredText guide by Sphinx <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
    - `autodoc Sphinx extension <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_
    - `Example Google Style Python Docstrings <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_

Docstrings
-------------
Use the Google style for Python docstrings, with types included in the docstrings.
Here are some examples for docstrings.

For Function
-------------
For functions, use the standard Google docstring style.

.. code-block:: python

    """
    Description of the function.

    Args:
        arg1 (``str``): description...
        arg2 (``bool``, optional): description...

    Returns:
        ``str``: description...
    
    Raises:
        SomeException: description...
    """

For Class
------------
- If a class has custom signals, define them in the ``Signals`` section.

Signal names should be in double quotes.
In brackets, indicate the custom arguments that the signal passes to the callback.

- If a class has custom properties, define them in the ``Properties`` section.

In brackets, indicate the property type and ``read-only`` or ``read-write``.

.. code-block:: python

    """
    This is an example docstring for a class.

    .. warning::
        This is a warning.

    Signals:
        - **"some-signal"** (): Emitted when the application is deleted.
        - **"arg-signal"** (``int``): Emitted when the xD. Passes an ``int`` as an argument.

    Properties:
        - **stream** (:class:`~ignis.some_class.SomeClass`, read-only): An instance of :class:`~ignis.some_class.SomeClass`.
        - **application_id** (``bool``, read-write): Whether to do something or not.
    """

Building documentation
-------------------------

Install dependencies

.. code-block:: bash

    pip install -r docs/requirements.txt

Build

.. code-block:: bash

    cd docs
    make html

Built documentation will be stored at ``_build/html``.