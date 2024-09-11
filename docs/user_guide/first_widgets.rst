First widgets
===============

First of all, let's create a config file in the default location.
The default config file is located at ``~/.config/ignis/config.py``.
You can create it using your file manager or the terminal with the command below.

.. code-block:: bash

    touch ~/.config/ignis/config.py

Open this file with your code editor.

Now, let's create the first window and display some text on it.

.. code-block:: python
    
    from ignis.widgets import Widget
    
    Widget.Window(
        namespace="some-window",  # the name of the window (not title!)
        child=Widget.Label(  # we set Widget.Label as the child widget of the window
            label="Hello world!"  # define text here
        ),
    )

.. info::
    Window is a top-level widget that contains all other widgets.

A list of all parameters  is provided here: :class:`~ignis.widgets.Widget.Window`. 
Feel free to experiment with them.

In this example, we used the ``Widget`` class, which provides access to all other widgets.

Some common widgets
---------------------

:class:`~ignis.widgets.Widget.Label`
--------------------------------------
A widget that displays text.

.. code-block:: python

    Widget.Label(label="some text")

:class:`~ignis.widgets.Widget.Box`
-----------------------------------
A layout container that can contain multiple child widgets and arrange them either vertically or horizontally.
By default, it places children horizontally. To place them vertically, set ``vertical`` to ``True``.

.. code-block:: python

    Widget.Box(
        vertical=False, # or True
        spacing=10,
        child=[Widget.Label(label="first label"), Widget.Label(label="second label")]
    )

:class:`~ignis.widgets.Widget.Button`
-----------------------------------------
I think from the name it's clear what kind of widget this is.
You can set a label for the button or use a custom child.

.. code-block:: python

    Widget.Button(
        label="click me", 
        on_click=lambda x: print("clicked!")
    )


.. code-block:: python

    Widget.Button(
        child=Widget.Label(label="test"),
        on_click=lambda x: print("clicked22!")
    )


:class:`~ignis.widgets.Widget.Icon`
-----------------------------------------
In GTK, there are built-in icons that you can access by name, so you probably won't need icons from nerd fonts.
To find out the names of the icons, you can use ``gtk4-icon-browser`` (you need to install ``gtk4-demos`` package).

.. code-block:: python

    Widget.Icon(
        image="audio-volume-high-symbolic"
    )
