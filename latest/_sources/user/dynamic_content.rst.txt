Dynamic content
=================

Static text can be boring, so let's add some dynamic elements!

.. code-block:: python

    import datetime
    from ignis.widgets import Widget
    from ignis.utils import Utils

    def update_label(clock_label: Widget.Label) -> None:
        text = datetime.datetime.now().strftime("%H:%M:%S")
        clock_label.set_label(text)

    def bar(monitor: int) -> Widget.Window:
        clock_label = Widget.Label()

        Utils.Poll(1000, lambda x: update_label(clock_label))

        return Widget.Window(
            namespace=f"some-window-{monitor}",
            monitor=monitor,
            child=Widget.Box(
                vertical=True,
                spacing=10,
                child=[clock_label],
            ),
        )

This code updates label every second with the current time (using built-in Python module ``datetime``).

Signals
-------------

Polling data every second isn't always ideal, as it can negatively impact performance.
This is where **signals** are useful. 
Signals let us call a callback only when an event occurs (like ``on_click`` in ``Widget.Button``).

Let's consider services, which often have both **signals** and **properties**.

Here's an example using the :class:`~ignis.services.mpris.MprisService`:

.. code-block:: python

    from ignis.services.mpris import MprisService

    mpris = MprisService.get_default()

    mpris.connect("player_added", lambda x, player: print(player.desktop_entry, player.title))
    #                                    ^    ^
    # Signals always pass the GObject they belong to as the first argument to the callback.
    # In this case, MprisPlayer is the second argument of the signal.

Now, open any media player (like a video on YouTube or music on Spotify). 
Magic! The player name and title will be printed.

.. hint::

    To manually emit (trigger) a signal, use the ``.emit()`` method and pass the signal name to it.

Binding
-----------

Next, let's **bind** a property.
Use the ``.bind()`` method, passing the property name as the first argument, and optionally a **transform** function.

.. code-block:: python

    from ignis.services.audio import AudioService
    from ignis.widgets import Widget

    audio = AudioService.get_default()

    def bar(monitor: int) -> Widget.Window:
        return Widget.Window(
            namespace=f"some-window-{monitor}",
            monitor=monitor,
            child=Widget.Box(
                child=[
                    Widget.Label(label="Current volume: "),
                    Widget.Label(
                        label=audio.speaker.bind("volume", lambda value: str(value))  # this function converts the value to a string
                    )
                ]
            ),
        )

Try changing the speaker volume using a tool like ``pavucontrol``.

When the property changes, the transform function (if provided) will be called with the new value, and it should return the processed result.

``notify`` signal
------------------
The ``notify`` is a special signal that emits when a property changes.
To connect to it, use the following syntax: ``"notify::PROPERTY-NAME"``.

.. danger::

    Make sure to use ``-`` instead of ``_`` in the property name. 
    Otherwise, the signal will not be triggered.

.. code-block:: python

    mpris.connect("notify::players", lambda x, y: print(x.players))