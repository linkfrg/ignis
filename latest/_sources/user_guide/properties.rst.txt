Properties
===============

Most classes in Ignis have properties.
These properties can have specific types (int, str, float), can be read-write or read-only, and can be optional or required.

In PyGObject, you typically use the special props attribute to access GObject properties. 
However, in Ignis, you don't need to use this attribute. 
Instead, you can access GObject properties using the standard Python approach.

.. code-block:: python

    widget = Widget.Label(label="Hello world!")
    print(widget.label) # prints: "Hello world!"

To set a property, you can use the assignment operator ``=`` or a method that starts with ``set_``.

.. code-block:: python
    
    widget.label = "test"
    print(widget.label) # prints: "test"
    widget.set_label("ignis") # this also works
    print(widget.label) # prints: "ignis"

