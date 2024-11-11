from gi.repository import Gtk, GLib  # type: ignore


class WindowNotFoundError(Exception):
    """
    Raised when a window is not found.
    """

    def __init__(self, window_name: str, *args) -> None:
        self._window_name = window_name
        super().__init__(f'No such window: "{window_name}"', *args)

    @property
    def window_name(self) -> str:
        """
        - required, read-only

        The name of the window.
        """
        return self._window_name


class WindowAddedError(Exception):
    """
    Raised when a window is already added to the application.
    """

    def __init__(self, window_name: str, *args) -> None:
        self._window_name = window_name
        super().__init__(f'Window already added: "{window_name}"', *args)

    @property
    def window_name(self) -> str:
        """
        - required, read-only

        The name of the window.
        """
        return self._window_name


class ServiceNotFoundError(Exception):
    """
    Raised when a service with the given name is not found.
    """

    def __init__(self, service_name: str, *args: object) -> None:
        self._service_name = service_name
        super().__init__(f'No such service "{service_name}"', *args)

    @property
    def service_name(self) -> str:
        """
        - required, read-only

        The name of the service.
        """
        return self._service_name


class GvcNotFoundError(Exception):
    """
    Raised when Gvc is not found.
    """

    def __init__(self, *args) -> None:
        super().__init__(
            "Gvc not found! To use the audio service, ensure that Ignis is installed correctly",
            *args,
        )


class HyprlandIPCNotFoundError(Exception):
    """
    Raised when Hyprland IPC is not found.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "Hyprland IPC not found! To use the Hyprland service, ensure that Hyprland is running",
            *args,
        )


class NetworkManagerNotFoundError(Exception):
    """
    Raised when NetworkManager is not found.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "NetworkManager not found! To use the network service, install NetworkManager",
            *args,
        )


class OptionNotFoundError(Exception):
    """
    Raised when an option is not found.
    """

    def __init__(self, option_name: str, *args) -> None:
        self._option_name = option_name
        super().__init__(f'No such option: "{option_name}"', *args)

    @property
    def option_name(self) -> str:
        """
        - required, read-only

        The name of the option.
        """
        return self._option_name


class OptionExistsError(Exception):
    """
    Raised when an option already exists.
    """

    def __init__(self, option_name: str, *args) -> None:
        self._option_name = option_name
        super().__init__(f'Option already exists: "{option_name}"', *args)

    @property
    def option_name(self) -> str:
        """
        - required, read-only

        The name of the option.
        """
        return self._option_name


class OptionsGroupNotFoundError(Exception):
    """
    Raised when an options group is not found.
    """

    def __init__(self, options_group: str, *args) -> None:
        self._options_group = options_group
        super().__init__(f'No such options group: "{options_group}"', *args)

    @property
    def options_group(self) -> str:
        """
        - required, read-only

        The name of the options group.
        """
        return self._options_group


class OptionsGroupExistsError(Exception):
    """
    Raised when an options group exists.
    """

    def __init__(self, options_group: str, *args) -> None:
        self._options_group = options_group
        super().__init__(f'Options groups already exists: "{options_group}"', *args)

    @property
    def options_group(self) -> str:
        """
        - required, read-only

        The name of the options group.
        """
        return self._options_group


class GstNotFoundError(Exception):
    """
    Raised when GStreamer is not found.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "GStreamer not found! To use the recorder service, install GStreamer", *args
        )


class GstPluginNotFoundError(Exception):
    """
    Raised when a GStreamer plugin is not found.
    """

    def __init__(self, plugin_name: str, plugin_package: str, *args) -> None:
        self._plugin_name = plugin_name
        self._plugin_package = plugin_package
        super().__init__(
            f"{plugin_name} GStreamer plugin not found! To use the recorder service, install {plugin_package}",
            *args,
        )

    @property
    def plugin_name(self) -> str:
        """
        - required, read-only

        The name of the plugin.
        """
        return self._plugin_name

    @property
    def plugin_package(self) -> str:
        """
        - required, read-only

        The package name of the plugin.
        """
        return self._plugin_package


class SassCompilationError(Exception):
    """
    Raised when Dart Sass compilation fails.
    """

    def __init__(self, stderr: str, *args: object) -> None:
        self._stderr = stderr
        super().__init__(f"SASS compilation error:\n{stderr}", *args)

    @property
    def stderr(self) -> str:
        """
        - required, read-only

        The stderr output from Dart Sass.
        """
        return self._stderr


class DartSassNotFoundError(Exception):
    """
    Raised when Dart Sass is not found.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "Dart Sass not found! To compile SCSS/SASS, install dart-sass", *args
        )


class MonitorNotFoundError(Exception):
    """
    Raised when a monitor with the given ID is not found.
    """

    def __init__(self, monitor_id: int, *args: object) -> None:
        self._monitor_id = monitor_id
        super().__init__(f"No such monitor with id: {monitor_id}", *args)

    @property
    def monitor_id(self) -> int:
        """
        - required, read-only

        The ID of the monitor.
        """
        return self._monitor_id


class LayerShellNotSupportedError(Exception):
    """
    Raised when the Layer Shell protocol is not supported.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "zwlr_layer_shell_v1 is not supported! Ensure you are running a Wayland compositor that implements the zwlr_layer_shell_v1 protocol",
            *args,
        )


class IgnisNotRunningError(Exception):
    """
    Raised when Ignis is not running.
    """

    def __init__(self, *args: object) -> None:
        super().__init__("Ignis is not running", *args)


class DBusMethodNotFoundError(Exception):
    """
    Raised when a D-Bus method is not found or not registered.
    """

    def __init__(self, method_name: str, *args: object) -> None:
        self._method_name = method_name
        super().__init__(
            f'No such registered D-Bus method with name: "{method_name}"', *args
        )

    @property
    def method_name(self) -> str:
        """
        - required, read-only

        The name of the D-Bus method.
        """
        return self._method_name


class DBusPropertyNotFoundError(Exception):
    """
    Raised when a D-Bus property is not found or not registered.
    """

    def __init__(self, property_name: str, *args: object) -> None:
        self._property_name = property_name
        super().__init__(
            f'No such registered D-Bus property with name: "{property_name}"', *args
        )

    @property
    def property_name(self) -> str:
        """
        - required, read-only

        The name of the D-Bus property.
        """
        return self._property_name


class DisplayNotFoundError(Exception):
    """
    Raised when the display is not found (e.g., a Wayland compositor is not running).
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "Display not found! Ensure you are running a Wayland compositor", *args
        )


class StylePathNotFoundError(Exception):
    """
    Raised when the style path is not found / not applied to the application.
    """

    def __init__(self, style_path: str, *args: object) -> None:
        self._style_path = style_path
        super().__init__(f'Style path is not found: "{style_path}"', *args)

    @property
    def style_path(self) -> str:
        """
        - required, read-only

        Path to the .css/.scss/.sass file.
        """
        return self._style_path


class StylePathAppliedError(Exception):
    """
    Raised when the style path is already applied to the application.
    """

    def __init__(self, style_path: str, *args: object) -> None:
        self._style_path = style_path
        super().__init__(f'Style path is already added: "{style_path}"', *args)

    @property
    def style_path(self) -> str:
        """
        - required, read-only

        Path to the .css/.scss/.sass file.
        """
        return self._style_path


class Gtk4LayerShellNotFoundError(Exception):
    """
    Raised when GTK4 Layer Shell is not found.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "GTK4 Layer Shell is not found! To use Ignis, first install it", *args
        )


class CssParsingError(Exception):
    """
    Raised when a CSS parsing error occurs.
    """

    def __init__(
        self, section: Gtk.CssSection, gerror: GLib.GError, *args: object
    ) -> None:
        self._section = section
        self._gerror = gerror
        super().__init__(f"{section.to_string()}: {gerror.message}", *args)

    @property
    def section(self) -> Gtk.CssSection:
        """
        - required, read-only

        The section the error happened in.
        """
        return self._section

    @property
    def gerror(self) -> GLib.GError:
        """
        - required, read-only

        The parsing error.
        """
        return self._gerror


class AnotherNotificationDaemonRunningError(Exception):
    """
    Raised when another notification daemon is running.
    """

    def __init__(self, name: str, *args: object) -> None:
        self._name = name
        super().__init__(
            f"Another notification daemon is already running: {name}", *args
        )

    @property
    def name(self) -> str:
        """
        - required, read-only

        The name of the currenly running notification daemon.
        """
        return self._name


class AnotherSystemTrayRunningError(Exception):
    """
    Raised when another system tray is running.
    """

    def __init__(self, name: str, *args: object) -> None:
        self._name = name
        super().__init__(f"Another system tray is already running: {name}", *args)

    @property
    def name(self) -> str:
        """
        - required, read-only

        The name of the currenly running system tray.
        """
        return self._name


class UPowerNotRunningError(Exception):
    """
    Raised when UPower is not running.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "UPower is not running! To use the UPower Service, install UPower and run it",
            *args,
        )
