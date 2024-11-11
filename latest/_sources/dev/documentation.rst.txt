Documentation Guidelines
========================

Ignis uses the `Sphinx <https://www.sphinx-doc.org/en/master/>`_ documentation generator
with the `autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_ 
extension to generate documentation from Python docstrings.

.. hint::
    Sphinx uses the reStructuredText markup language.
    Here are some useful resources to learn more about it:

    - `reStructuredText guide by Sphinx <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
    - `Example Google Style Python Docstrings <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_

Docstrings
-------------
Use the Google style for Python docstrings, with types included in them.
Here are some examples for functions and classes.

Functions
~~~~~~~~~~~~~~~~
For functions, use the standard Google docstring style.
Type hints will be added automatically.

.. code-block:: python

    def some_func(arg1: int, arg2: str) -> str:
        """
        Description of the function.

        Args:
            arg1: Description...
            arg2: Description 2...

        Returns:
            The description of the return value...
        
        Raises:
            SomeException: If this condition is true...
        """
        pass

General Classes
~~~~~~~~~~~~~~~~

- Signals:

    If a class has custom signals, add docstrings to the functions decorated with ``@GObject.Signal`` respectively.

    At the top of the docstring indicate that it's signal: ``- Signal``.

    Also, if the signal have custom arguments, define them in the ``Args`` section.

- Properties:

    If a class has custom properties, add docstrings to the functions decorated with ``@GObject.Object`` or ``@property`` respectively.

    At the top of the docstring indicate ``read-only`` / ``read-write``, ``optional`` / ``required`` / ``not argument``.

    .. note::
        You shouldn't specify ``optional`` / ``required`` / ``not argument``
        in properties of Services and classes related to them, since the user shouldn't initialize them manually.

- If possible, please provide a code example.

.. code-block:: python

    class SomeClass:
        """
        This is an example docstring for a class.
        Further info goes here...
        """

    @GObject.Signal
    def some_signal(self):
        """
        - Signal

        Emitted when the something happens.
        """

    @GObject.Signal(arg_types=(int,))
    def arg_signal(self):
        """
        - Signal

        Emitted when the something another happens.

        Args:
            some_arg (``int``): Description of the argument...
        """

    @GObject.Property
    def some_prop(self) -> int:
        """
        - optional, read-only
        """
        ...

    @GObject.Property
    def rw_prop(self) -> str:
        """
        - optional, read-write
        """
        ...

    @rw_prop.setter
    def rw_prop(self, value: str) -> None:
        ...

Widgets
~~~~~~~~~~~~~~~~

- Use the same patterns as described above for general classes.
- Specify the base widget using the ``:class:`` directive.

.. code-block:: python

    class SomeWidget:
        """
        Bases: :class:`Gtk.WIDGET_NAME`

        The description of the widget.

        .. code-block:: python

            Widget.WIDGET_NAME(
                prop1="asd",
                prop2=12
            )
        """
        ... # rest of stuff goes here

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