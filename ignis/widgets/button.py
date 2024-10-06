from __future__ import annotations
from gi.repository import Gtk, GObject  # type: ignore
from ignis.base_widget import BaseWidget
from typing import Callable


class Button(Gtk.Button, BaseWidget):
    """
    Bases: `Gtk.Button <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Button.html>`_.

    A button.

    Properties:
        - **on_click** (``Callable``, optional, read-write): The function to call on left click.
        - **on_right_click** (``Callable``, optional, read-write): The function to call on right click.
        - **on_middle_click** (``Callable``, optional, read-write): The function to call on middle click.

    .. code-block:: python

        Widget.Button(
            child=Widget.Label(label="button"),
            on_click=lambda self: print(self),
            on_right_click=lambda self: print(self),
            on_middle_click=lambda self: print(self),
        )
    """

    __gtype_name__ = "IgnisButton"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.Button.__init__(self)
        self._on_click: Callable | None = None
        self._on_right_click: Callable | None = None
        self._on_middle_click: Callable | None = None

        self.__right_click_controller: Gtk.GestureClick | None = None
        self.__middle_click_controller: Gtk.GestureClick | None = None

        BaseWidget.__init__(self, **kwargs)
        self.connect("clicked", lambda x: self.on_click(x) if self.on_click else None)

    def __init_controller(self, button: int, callback: Callable) -> Gtk.GestureClick:
        def on_pressed(gesture_click: Gtk.GestureClick, n_press, x, y) -> None:
            gesture_click.set_state(Gtk.EventSequenceState.CLAIMED)
            callback(self)

        controller = Gtk.GestureClick()
        controller.set_button(button)
        self.add_controller(controller)
        controller.connect("pressed", on_pressed)
        return controller

    @GObject.Property
    def on_click(self) -> Callable:
        return self._on_click

    @on_click.setter
    def on_click(self, value: Callable) -> None:
        self._on_click = value

    @GObject.Property
    def on_right_click(self) -> Callable:
        return self._on_right_click

    @on_right_click.setter
    def on_right_click(self, value: Callable) -> None:
        self._on_right_click = value
        if not self.__right_click_controller:
            self.__right_click_controller = self.__init_controller(
                3, self._on_right_click
            )

    @GObject.Property
    def on_middle_click(self) -> Callable:
        return self._on_middle_click

    @on_middle_click.setter
    def on_middle_click(self, value: Callable) -> None:
        self._on_middle_click = value
        if not self.__middle_click_controller:
            self.__middle_click_controller = self.__init_controller(
                2, self._on_middle_click
            )
