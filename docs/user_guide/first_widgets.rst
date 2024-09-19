First widgets
===============

Once you have installed Ignis, it's time to create your first widget!

First, create a configuration file in the default location.
The default config file is located at ``~/.config/ignis/config.py``.
Create this file and open it using your favorite code editor.

The window
------------

The window is the top-level widget that holds all other widgets.

.. code-block:: python
    
    from ignis.widgets import Widget
    
    Widget.Window(
        namespace="some-window",  # the name of the window (not title!)
        child=Widget.Label(  # we set Widget.Label as the child widget of the window
            label="Hello world!"  # define text here
        ),
    )

Copy and paste this code into your config file, 
and then run Ignis using ``ignis``.

You should see a window that looks like this:

.. image:: /_static/images/user_guide/hello_world.png
    :alt: "Hello world!" window

This code imports the universal ``Widget`` class, which is used to access all widgets available in Ignis.
To initialize a widget, simply call it: ``Widget.WIDGET_NAME()``.
Using keyword arguments (kwargs), you can set properties of the widget.

A list of all properties is provided here: :class:`~ignis.widgets.Widget.Window`. 
Feel free to experiment with them.

Boxes
---------------------
A box is a layout container that can hold multiple child widgets and arrange them either vertically or horizontally.
By default, it arranges children horizontally. To arrange them vertically, set ``vertical`` to ``True``.

Let's add some boxes to the window.

.. code-block:: python

    from ignis.widgets import Widget

    Widget.Window(
        namespace="some-window",
        child=Widget.Box(
            vertical=True,  # this box is vertical
            spacing=10,  # add some spacing between widgets
            child=[  # define list of child widgets here
                Widget.Label(label="This is the first child of the first box"),
                Widget.Box(
                    spacing=26,
                    child=[
                        Widget.Label(label="This is the first child of the second box"),
                        Widget.Label(label="Second child (by default this box child will be added horizontally)"),
                    ]
                ),
            ],
        ),
    )

Result:

.. image:: /_static/images/user_guide/boxes.png
    :alt: Boxes example image

Buttons (and Callbacks!)
-------------------------

Let's add a couple of buttons to our window that will perform actions when pressed.

.. code-block:: python

    from ignis.widgets import Widget

    def complex_operation(x):
        print("Doing something 1")
        print("Doing something 2")
        print("Doing something 3")


    # you can assign widgets to variables
    button1 = Widget.Button(
        child=Widget.Label(label="Click me!"),
        on_click=lambda x: print("you clicked the button 1"),
    )
    button2 = Widget.Button(
        child=Widget.Label(label="Don't listen him! Click me!"), on_click=complex_operation
    )
    button3 = Widget.Button(
        child=Widget.Label(label="Click me and text will change"),
        on_click=lambda x: x.child.set_label("Text changed!"),
    )

    Widget.Window(
        namespace="some-window",
        child=Widget.Box(
            vertical=True,
            spacing=10,
            child=[
                Widget.Label(label="Click buttons)))"),
                Widget.Box(
                    spacing=26,
                    child=[
                        button1,
                        button2,
                        button3,
                    ],
                ),
            ],
        ),
    )

.. hint::
    Use ``lambda`` functions for simple operations

In this example, ``x`` is just an argument.
For callbacks, an instance of the class is often passed as the first argument (in our case, it is the button itself).
Of course, you can interact with this instance in some way (as shown with button number 3).

Reusable Widgets
-------------------

In previous examples, widgets are declared as single instances.
One ``Widget.Label`` cannot be added to two boxes at the same time.
But what if you have two monitors and want to display the bar on both?
The solution is to create functions that return widget instances.

.. code-block:: python

    from ignis.widgets import Widget

    def complex_operation(x):
        print("Doing something 1")
        print("Doing something 2")
        print("Doing something 3")

    def bar(monitor: int) -> Widget.Window:  # type hinting is good practice!
        button1 = Widget.Button(
            child=Widget.Label(label="Click me!"),
            on_click=lambda x: print("you clicked the button 1"),
        )
        button2 = Widget.Button(
            child=Widget.Label(label="Don't listen him! Click me!"), on_click=complex_operation
        )
        button3 = Widget.Button(
            child=Widget.Label(label="Click me and text will change"),
            on_click=lambda x: x.child.set_label("Text changed!"),
        )

        return Widget.Window(
            namespace=f"some-window-{monitor}",  # the namespace must be unique
            monitor=monitor,
            child=Widget.Box(
                vertical=True,
                spacing=10,
                child=[
                    Widget.Label(label="Click buttons)))"),
                    Widget.Box(
                        spacing=26,
                        child=[
                            button1,
                            button2,
                            button3,
                        ],
                    ),
                ],
            ),
        )

    # initialize two bars for two monitors
    bar(0)
    bar(1)

.. hint::
    Need more widgets? See them in the `API Reference <../api_reference/widgets/index.html>`_.

Properties
-------------

GObject properties can be accessed or set using the standard Python approach.

.. code-block:: python

    widget = Widget.Label(label="Hello world!")
    print(widget.label) # prints: "Hello world!"

To set a property, you can use the assignment operator ``=`` or a method that starts with ``set_``.

.. code-block:: python

    widget = Widget.Label()
    
    widget.label = "test"
    print(widget.label) # prints: "test"
    widget.set_label("ignis") # this also works
    print(widget.label) # prints: "ignis"

Services
------------

Ignis includes built-in `Services <../api_reference/services/index.html>`_, 
which allow you to interact with various system components, 
such as controlling audio, managing networks, handling notifications, and more.

