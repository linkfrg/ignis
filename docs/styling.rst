Styling
========
Ignis supports both CSS and SCSS.

Using CSS/SCSS file
--------------------

To get started, add the following to your config:

.. code-block:: python

    from ignis.app import app

    app.apply_css("PATH/TO/CSS_FILE")

For example, we will use ``~/.config/ignis/style.scss``:

.. code-block:: python

    import os
    from ignis.app import app

    app.apply_css(os.path.expanduser("~/.config/ignis/style.scss"))

Now, you can add a CSS class to any widget and style it in the CSS file.
To add CSS classes to a widget, use the ``css_classes`` property.

.. code-block:: python
    
    Widget.Label(
        label="hello",
        css_classes=["my-label"]
    )

In style.scss:

.. code-block:: css

    .my-label {
        background-color: red;
    }

Using the ``style`` property
------------------------------

.. warning::
    The ``style`` property does not support SCSS features, only CSS.

.. code-block:: python

    Widget.Label(
        label="hello",
        style="background-color: black;"
    )