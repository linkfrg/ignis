Dynamic content
================

Signals
------------
In GObject, we have a concept called "signals".

Signals are system for registering callbacks for specific events.
For example, when a user clicks a button, the program can perform a specific action. 
Similarly, when a property of an object changes, the program can respond accordingly.

To connect to signals, use ``.connect()`` method on GObject that has the signal you need. 
Pass a callback function that will be called when the signal is emitted.
Signals always pass the GObject they belong to as the first argument to the callback.
Services also have their own signals, which are listed on their respective documentation pages.
Additionally, signals can have custom arguments. 
In example below, ``"player_added"`` signal passes an instance of :class:`~ignis.services.mpris.MprisPlayer` as the second argument to the callback.

Here, we will use the :class:`~ignis.services.mpris.MprisService` as an example.

.. code-block:: python

    from ignis.service import Service

    mpris = Service.get("mpris")

    mpris.connect("player_added", lambda x, player: print(player.desktop_entry, player.title))

Now, try opening any media player (for example, video on youtube or music in spotify).
Magic! The player name and title will be printed.

To emit (call) signal manually, use the ``.emit()`` method and pass the signal name to it.

``notify`` signal
------------------
The ``notify`` is a special signal that emits when a property changes.
To connect to it, use the following syntax: ``"notify::PROPERTY-NAME"``.

.. danger::

    Use ``-`` instead of ``_``. Otherwise, signal callback will never be called.

.. code-block:: python

    mpris.connect("notify::players", lambda x, y: print(x.players))



Binding
---------------

You can call the ``.bind()`` method on widgets, services, or utils and pass a property name.
This method returns a :class:`~ignis.gobject.Binding`, which you can use to set a property value for a widget.

.. code-block:: python

    from ignis.services import Service
    from ignis.widgets import Widget

    audio = Service.get("audio")

    Widget.Label(label=audio.speaker.bind("volume", transform=lambda value: str(value)))

This code creates a binding. 
Now, the label of ``Widget.Label`` will depend on the speaker's volume.
The ``label`` property accepts a ``str``, but ``speaker.volume`` is an ``int``.
So, we provide a transform function to ``.bind()``,
which converts the speaker volume to a string.