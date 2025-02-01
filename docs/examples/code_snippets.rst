Code Snippets
==============

This page provides useful code snippets to help you implementing additional functionality. 

Clicking outside of a window
----------------------------

A common use case is to close a window.

.. code-block:: python

    Widget.Window(
        namespace="my-window",
        anchor=["left", "right", "top", "bottom"],  # to make a window fullscreen
        child=Widget.Overlay(
            child=Widget.Button(
                vexpand=True,
                hexpand=True,
                can_focus=False,
                on_click=lambda x: CALLBACK, # e.g., app.close_window("my-window")
            ),
            overlays=[ACTUAL_CONTENT],
        ),
    )

Replace ``ACTUAL_CONTENT`` with the actual widgets you want to put in the window.

.. warning::
    If ``ACTUAL_CONTENT`` fills all of the screen, 
    set ``valign``` and ``halign`` with values other than ``fill`` (e.g., ``center``).