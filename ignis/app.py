from __future__ import annotations
import os
import sys
from ignis.dbus import DBusService
from ignis.utils import Utils
from loguru import logger
from gi.repository import Gtk, Gdk, Gio, GObject, GLib  # type: ignore
from ignis.gobject import IgnisGObject
from ignis.exceptions import (
    WindowAddedError,
    WindowNotFoundError,
    DisplayNotFoundError,
    StylePathNotFoundError,
    StylePathAppliedError,
)
from ignis.logging import configure_logger
from ignis.widgets.window import Window

class IgnisApp(Gtk.Application, IgnisGObject):
    """
    Application class.

    .. danger::

        Do not initialize this class!
        Instead, use the already initialized instance as shown below.

    .. code-block:: python

        from ignis.app import IgnisApp

        app = IgnisApp.get_default()

    Signals:
        - **"ready"** (): Emitted when the configuration has been parsed.
        - **"quit"** (): Emitted when Ignis has finished running.

    Properties:
        - **windows** (list[:class:`~ignis.widgets.Widget.Window`], read-only): List of windows.
        - **is_ready** (``bool``, read-only): Whether configuration is parsed and app is ready.
        - **autoreload_config** (``bool``, read-write, default: ``True``): Whether to automatically reload the configuration when it changes (only .py files).
        - **autoreload_css** (``bool``, read-write, default: ``True``): Whether to automatically reload the CSS style when it changes (only .css/.scss/.sass files).
    """

    __gsignals__ = {
        "ready": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "quit": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    _instance: IgnisApp | None = None  # type: ignore

    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id="com.github.linkfrg.ignis",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        IgnisGObject.__init__(self)

        self.__dbus = DBusService(
            name="com.github.linkfrg.ignis",
            object_path="/com/github/linkfrg/ignis",
            info=Utils.load_interface_xml("com.github.linkfrg.ignis"),
        )

        self.__dbus.register_dbus_method(name="OpenWindow", method=self.__OpenWindow)
        self.__dbus.register_dbus_method(name="CloseWindow", method=self.__CloseWindow)
        self.__dbus.register_dbus_method(
            name="ToggleWindow", method=self.__ToggleWindow
        )
        self.__dbus.register_dbus_method(name="Quit", method=self.__Quit)
        self.__dbus.register_dbus_method(name="Inspector", method=self.__Inspector)
        self.__dbus.register_dbus_method(name="RunPython", method=self.__RunPython)
        self.__dbus.register_dbus_method(name="RunFile", method=self.__RunFile)
        self.__dbus.register_dbus_method(name="Reload", method=self.__Reload)
        self.__dbus.register_dbus_method(name="ListWindows", method=self.__ListWindows)

        self._config_path: str | None = None
        self._css_providers: dict[
            str, Gtk.CssProvider
        ] = {}  # {style_path: Gtk.CssProvider}
        self._windows: dict[str, Window] = {}
        self._autoreload_config: bool = True
        self._autoreload_css: bool = True
        self._is_ready = False

    def __watch_config(self, path: str, event_type: str) -> None:
        if event_type == "changed":  # "changed" event is called multiple times
            return

        if not os.path.isdir(path) and "__pycache__" not in path:
            extension = os.path.splitext(path)[1]
            if extension == ".py" and self.autoreload_config:
                self.reload()
            elif extension in (".css", ".scss", ".sass") and self.autoreload_css:
                self.reload_css()

    @classmethod
    def get_default(cls: type[IgnisApp]) -> IgnisApp:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @GObject.Property
    def is_ready(self) -> bool:
        return self._is_ready

    @GObject.Property
    def windows(self) -> list[Window]:
        return list(self._windows.values())

    @GObject.Property
    def autoreload_config(self) -> bool:
        return self._autoreload_config

    @autoreload_config.setter
    def autoreload_config(self, value: bool) -> None:
        self._autoreload_config = value

    @GObject.Property
    def autoreload_css(self) -> bool:
        return self._autoreload_css

    @autoreload_css.setter
    def autoreload_css(self, value: bool) -> None:
        self._autoreload_css = value

    def _setup(self, config_path: str) -> None:
        """
        :meta private:
        """
        self._config_path = config_path

    def apply_css(self, style_path: str) -> None:
        """
        Apply a CSS/SCSS/SASS style from a path.
        If ``style_path`` has a ``.sass`` or ``.scss`` extension, it will be automatically compiled.
        Requires ``dart-sass`` for SASS/SCSS compilation.

        Args:
            style_path (``str``): Path to the .css/.scss/.sass file.

        Raises:
            StylePathAppliedError: if the given style path is already to the application.
            DisplayNotFoundError
        """

        display = Gdk.Display.get_default()

        if not display:
            raise DisplayNotFoundError()

        if style_path in self._css_providers:
            raise StylePathAppliedError(style_path)

        if not os.path.exists(style_path):
            raise FileNotFoundError(
                f"Provided style path doesn't exists: '{style_path}'"
            )

        if style_path.endswith(".scss") or style_path.endswith(".sass"):
            css_style = Utils.sass_compile(path=style_path)
        elif style_path.endswith(".css"):
            with open(style_path) as file:
                css_style = file.read()
        else:
            raise ValueError(
                'The "style_path" argument must be a path to a CSS, SASS, or SCSS file'
            )

        provider = Gtk.CssProvider()
        provider.load_from_string(css_style)

        Gtk.StyleContext.add_provider_for_display(
            display,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._css_providers[style_path] = provider

        logger.info(f"Applied css: {style_path}")

    def remove_css(self, style_path: str) -> None:
        """
        Remove the applied CSS/SCSS/SASS style by its path.

        Args:
            style_path (``str``): Path to the applied .css/.scss/.sass file.

        Raises:
            StylePathNotFoundError: if the given style path is not applied to the application.
            DisplayNotFoundError
        """

        display = Gdk.Display.get_default()
        if not display:
            raise DisplayNotFoundError()

        provider = self._css_providers.pop(style_path, None)

        if provider is None:
            raise StylePathNotFoundError(style_path)

        Gtk.StyleContext.remove_provider_for_display(
            display,
            provider,
        )

    def reset_css(self) -> None:
        """
        Reset all applied CSS/SCSS/SASS styles.

        Raises:
            DisplayNotFoundError
        """
        for style_path in self._css_providers.copy().keys():
            self.remove_css(style_path)

    def reload_css(self) -> None:
        """
        Reload all applied CSS/SCSS/SASS styles.

        Raises:
            DisplayNotFoundError
        """
        style_paths = self._css_providers.copy().keys()
        self.reset_css()

        for i in style_paths:
            self.apply_css(i)

    def do_activate(self) -> None:
        """
        :meta private:
        """
        self.hold()

        if not self._config_path:
            raise ValueError("Set up config_path before trying to run application")

        if not os.path.exists(self._config_path):
            raise FileNotFoundError(
                f"Provided config path doesn't exists: {self._config_path}"
            )

        config_dir = os.path.dirname(self._config_path)
        config_filename = os.path.splitext(os.path.basename(self._config_path))[0]

        logger.info(f"Using configuration file: {self._config_path}")

        self._monitor = Utils.FileMonitor(
            path=config_dir, callback=self.__watch_config, recursive=True
        )

        sys.path.append(config_dir)
        __import__(config_filename)

        self._is_ready = True
        self.emit("ready")
        logger.info("Ready.")

    def get_window(self, window_name: str) -> Window:
        """
        Get a window by name.

        Args:
            window_name (``str``): The window's namespace.

        Returns:
            :class:`~ignis.widgets.Widget.Window`: The window object.
        Raises:
            WindowNotFoundError: If a window with the given namespace does not exist.
        """
        window = self._windows.get(window_name, None)
        if window:
            return window
        else:
            raise WindowNotFoundError(window_name)

    def open_window(self, window_name: str) -> None:
        """
        Open (show) a window by its name.

        Args:
            window_name (``str``): The window's namespace.
        Raises:
            WindowNotFoundError: If a window with the given namespace does not exist.
        """
        window = self.get_window(window_name)
        window.set_visible(True)

    def close_window(self, window_name: str) -> None:
        """
        Close (hide) a window by its name.

        Args:
            window_name (``str``): The window's namespace.
        Raises:
            WindowNotFoundError: If a window with the given namespace does not exist.
        """
        window = self.get_window(window_name)
        window.set_visible(False)

    def toggle_window(self, window_name: str) -> None:
        """
        Toggle (change visibility to opposite state) a window by its name.

        Args:
            window_name (``str``): The window's namespace.
        Raises:
            WindowNotFoundError: If a window with the given namespace does not exist.
        """
        window = self.get_window(window_name)
        window.set_visible(not window.get_visible())

    def add_window(self, window_name: str, window: Window) -> None:  # type: ignore
        """
        Add a window.
        You typically shouldn't use this method, as windows are added to the app automatically.

        Args:
            window_name (``str``): The window's namespace.
            window (:class:`~ignis.widgets.Widget.Window`): The window instance.

        Raises:
            WindowAddedError: If a window with the given namespace already exists.
        """
        if window_name in self._windows:
            raise WindowAddedError(window_name)

        self._windows[window_name] = window
        window.connect("close-request", lambda x: self.remove_window(window_name))

    def remove_window(self, window_name: str) -> None:  # type: ignore
        """
        Remove a window by its name.
        The window will be removed from the application.

        Args:
            window_name (``str``): The window's namespace.

        Raises:
            WindowNotFoundError: If a window with the given namespace does not exist.
        """
        window = self._windows.pop(window_name, None)
        if not window:
            raise WindowNotFoundError(window_name)

    def reload(self) -> None:
        """
        Reload Ignis.
        """
        self.quit()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def quit(self) -> None:
        """
        Quit Ignis.
        """
        super().quit()
        self.emit("quit")
        logger.info("Quitting.")

    def inspector(self) -> None:
        """
        Open GTK Inspector.
        """
        Gtk.Window.set_interactive_debugging(True)

    def __call_window_method(self, _type: str, window_name: str) -> GLib.Variant:
        try:
            getattr(self, f"{_type}_window")(window_name)
            return GLib.Variant("(b)", (True,))
        except WindowNotFoundError:
            return GLib.Variant("(b)", (False,))

    def __OpenWindow(self, invocation, window_name: str) -> GLib.Variant:
        return self.__call_window_method("open", window_name)

    def __CloseWindow(self, invocation, window_name: str) -> GLib.Variant:
        return self.__call_window_method("close", window_name)

    def __ToggleWindow(self, invocation, window_name: str) -> GLib.Variant:
        return self.__call_window_method("toggle", window_name)

    def __ListWindows(self, invocation) -> GLib.Variant:
        return GLib.Variant("(as)", (tuple(self._windows),))

    def __RunPython(self, invocation, code: str) -> None:
        invocation.return_value(None)
        exec(code)

    def __RunFile(self, invocation, path: str) -> None:
        invocation.return_value(None)
        with open(path) as file:
            code = file.read()
            exec(code)

    def __Inspector(self, invocation) -> None:
        self.inspector()

    def __Reload(self, invocation) -> None:
        invocation.return_value(None)
        self.reload()

    def __Quit(self, invocation) -> None:
        self.quit()


def run_app(config_path: str, debug: bool) -> None:
    configure_logger(debug)

    app = IgnisApp.get_default()

    app._setup(config_path)

    try:
        app.run(None)
    except KeyboardInterrupt:
        pass  # app.quit() will be called automatically
