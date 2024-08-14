import cairo
from ignis.app import app
from gi.repository import Gtk, GObject
from ignis.base_widget import BaseWidget
from ignis.utils import Utils
from typing import List
from gi.repository import Gtk4LayerShell as GtkLayerShell
from ignis.exceptions import MonitorNotFoundError, LayerShellNotSupportedError


LAYER = {
    "background": GtkLayerShell.Layer.BACKGROUND,
    "bottom": GtkLayerShell.Layer.BOTTOM,
    "top": GtkLayerShell.Layer.TOP,
    "overlay": GtkLayerShell.Layer.OVERLAY,
}

KB_MODE = {
    None: GtkLayerShell.KeyboardMode.NONE,
    "none": GtkLayerShell.KeyboardMode.NONE,
    "exclusive": GtkLayerShell.KeyboardMode.EXCLUSIVE,
    "on_demand": GtkLayerShell.KeyboardMode.ON_DEMAND,
}


ANCHOR = {
    "bottom": GtkLayerShell.Edge.BOTTOM,
    "left": GtkLayerShell.Edge.LEFT,
    "right": GtkLayerShell.Edge.RIGHT,
    "top": GtkLayerShell.Edge.TOP,
}

EXCLUSIVITY = {
    "ignore": -1,
    "normal": 0,
    "exclusive": 1,
}


class Window(Gtk.Window, BaseWidget):
    """
    Bases: `Gtk.Window <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/Window.html>`_.

    The top-level widget that contains everything.

    Properties:
        - **namespace** (``str``, required, read-only): The name of the window, used to access it from the CLI and :class:`~ignis.app.ignisApp`. It must be unique. It is also the name of the layer.
        - **monitor** (``int``, optional, read-write): Monitor number on which to display the window. Raises :class:`~ignis.exceptions.MonitorNotFoundError` if the monitor with the given ID is not found.
        - **anchor** (``List[str]``, optional, read-write): List of anchors. If the list is empty, the window will be centered on the screen. Default: ``[]``.
        - **exclusivity** (``str``, optional, read-write): Define how the compositor should avoid occluding a window area with other surfaces/layers. Default: ``"normal"``.
        - **layer** (``str``, optional, read-write): Layer of the surface. Default: ``"top"``.
        - **kb_mode** (``str``, optional, read-write): Whether the window should receive keyboard events from the compositor. Default: ``"none"``.
        - **popup** (``bool``, optional, read-write): Whether the window should close on ESC. Works only if ``kb_mode`` is set to ``"exclusive"`` or ``"on_demand"``.

    **Anchors:**
        - **"bottom"**
        - **"left"**
        - **"right"**
        - **"top"**

    **Exclusivity:**
        - **"ignore"** : Completely ignore other surfaces. This allows you to overlap other surfaces.
        - **"normal"** : The window will have no extra space and do not overlap other surfaces.
        - **"exclusive"** : The compositor will reserve extra space for this window.

    **Layer:**
        - **"background"**
        - **"bottom"**
        - **"top"**
        - **"overlay"**

    **Keyboard mode:**
        - **"none"** : This window should not receive keyboard events.
        - **"exclusive"** : This window should have exclusive focus if it is on the top or overlay layer.
        - **"on_demand"** : The user should be able to focus and unfocus this window.

    Raises:
        LayerShellNotSupportedError: If the compositor does not support the Layer Shell protocol.
        MonitorNotFoundError: If an invalid ID is passed to the ``monitor`` property.

    .. code-block:: python

        Widget.Window(
            namespace="example_window",
            child=Widget.Label(label='heh'),
            monitor=0,
            anchor=["top", "right"],
            exclusive=True,
            layer="top",
            kb_mode="none",
            popup=False
        )

    """

    __gtype_name__ = "IgnisWindow"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        namespace: str,
        monitor: int = None,
        anchor: List[str] = None,
        exclusivity: str = "normal",
        layer: str = "top",
        kb_mode: str = "none",
        popup: bool = False,
        **kwargs,
    ):
        if not GtkLayerShell.is_supported():
            raise LayerShellNotSupportedError()

        Gtk.Window.__init__(self, application=app)
        GtkLayerShell.init_for_window(self)

        self._anchor = None
        self._exclusivity = None
        self._namespace = None
        self._layer = None
        self._kb_mode = None
        self._popup = None
        self._monitor = None
        self._input_width = -1
        self._input_height = -1

        self.anchor = anchor
        self.exclusivity = exclusivity
        self.namespace = namespace
        self.layer = layer
        self.kb_mode = kb_mode
        self.monitor = monitor
        self.popup = popup
        self.default_width = 2
        self.default_height = 2

        app.add_window(namespace, self)

        key_controller = Gtk.EventControllerKey()
        self.add_controller(key_controller)
        key_controller.connect("key-pressed", self.__close_popup)

        BaseWidget.__init__(self, **kwargs)

    def __close_popup(self, event_controller_key, keyval, keycode, state):
        if self._popup:
            if keyval == 65307:  # 65307 = ESC
                app.close_window(GtkLayerShell.get_namespace(self))

    @GObject.Property
    def anchor(self) -> list:
        return self._anchor

    @anchor.setter
    def anchor(self, value: list) -> None:
        self._anchor = value
        for i in value:
            GtkLayerShell.set_anchor(self, ANCHOR[i], 1)

    @GObject.Property
    def exclusivity(self) -> str:
        return self._exclusivity

    @exclusivity.setter
    def exclusivity(self, value: str) -> None:
        self._exclusive = value
        if value == "exclusive":
            GtkLayerShell.auto_exclusive_zone_enable(self)
        else:
            GtkLayerShell.set_exclusive_zone(self, EXCLUSIVITY[value])

    @GObject.Property
    def namespace(self) -> str:
        return self._namespace

    @namespace.setter
    def namespace(self, value: str) -> None:
        self._namespace = value
        GtkLayerShell.set_namespace(self, name_space=value)

    @GObject.Property
    def layer(self) -> str:
        return self._layer

    @layer.setter
    def layer(self, value: str) -> None:
        self._layer = value
        GtkLayerShell.set_layer(self, LAYER[value])

    @GObject.Property
    def kb_mode(self) -> str:
        return self._kb_mode

    @kb_mode.setter
    def kb_mode(self, value: str) -> None:
        self._kb_mode = value
        GtkLayerShell.set_keyboard_mode(self, KB_MODE[value])

    @GObject.Property
    def popup(self) -> bool:
        return self._popup

    @popup.setter
    def popup(self, value: bool) -> None:
        self._popup = value

    @GObject.Property
    def monitor(self) -> int:
        return self._monitor

    @monitor.setter
    def monitor(self, value: int) -> None:
        gdkmonitor = Utils.get_monitor(value)
        if gdkmonitor is None:
            raise MonitorNotFoundError(value)

        GtkLayerShell.set_monitor(self, gdkmonitor)
        self._monitor = value

    @GObject.Property
    def input_width(self) -> int:
        return self._input_width

    @input_width.setter
    def input_width(self, value: int) -> None:
        self._input_width = value
        self.__change_input_region()

    @GObject.Property
    def input_height(self) -> int:
        return self._input_height

    @input_height.setter
    def input_height(self, value: int) -> None:
        self._input_height = value
        self.__change_input_region()

    def __change_input_region(self) -> None:
        if self.input_width < 0:
            return

        if self.input_height < 0:
            return

        rectangle = cairo.RectangleInt(0, 0, self.input_width, self.input_height)
        region = cairo.Region(rectangle)
        self.get_surface().set_input_region(region)
