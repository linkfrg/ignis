Using Classes
=============

While functions are easier to use (especially for beginners in Python),
classes are more suitable for initializing new objects.

This approach has several benefits, such as better-structured code
and the ability to use ``self``, which is especially useful for complex widgets.

.. code-block:: python

    from ignis.widgets import Widget


    class Bar(Widget.Window):  # inheriting from Widget.Window
        __gtype_name__ = "MyBar"  # optional, this will change the widget's display name in the GTK inspector.

        def __init__(self, monitor: int):
            button1 = Widget.Button(
                child=Widget.Label(label="Click me!"),
                on_click=lambda x: print("you clicked the button 1"),
            )
            button2 = Widget.Button(
                child=Widget.Label(label="Close window"),
                on_click=lambda x: self.set_visible(False),  # you can use "self" - the window object itself
            )
            button3 = Widget.Button(
                child=Widget.Label(label="Custom function on self"),
                on_click=lambda x: self.some_func(),
            )

            super().__init__(  # calling the constructor of the parent class (Widget.Window)
                namespace=f"some-window-{monitor}",
                monitor=monitor,
                anchor=["left", "top", "right"],
                child=Widget.Box(
                    spacing=10,
                    child=[
                        Widget.Label(label="This window created using a custom class!"),
                        button1,
                        button2,
                        button3,
                    ],
                ),
            )

        def some_func(self) -> None:
            print("Custom function on self!")

    # initialize
    Bar(0)

In fact, you can use both classes and functions.  
Using classes instead of functions is not mandatory but is recommended.

.. seealso::
    For advanced usage, you can override methods, add custom properties, and define signals.  
    Knowledge of Python OOP and PyGObject is encouraged.