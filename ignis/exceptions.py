class WindowNotFoundError(Exception):
    """
    Raised when a window is not found.

    Properties:
        - **window_name** (``str``, required, read-only): The name of the window.
    """

    def __init__(self, window_name: str, *args) -> None:
        self._window_name = window_name
        super().__init__(f'No such window: "{window_name}"', *args)

    @property
    def window_name(self) -> str:
        return self._window_name


class WindowAddedError(Exception):
    """
    Raised when a window is already added to the application.

    Properties:
        - **window_name** (``str``, required, read-only): The name of the window.
    """

    def __init__(self, window_name: str, *args) -> None:
        self._window_name = window_name
        super().__init__(f'Window already added: "{window_name}"', *args)

    @property
    def window_name(self) -> str:
        return self._window_name


class ServiceNotFoundError(Exception):
    """
    Raised when a service with the given name is not found.

    Properties:
        - **service_name** (``str``, required, read-only): The name of the service.
    """

    def __init__(self, service_name: str, *args: object) -> None:
        self._service_name = service_name
        super().__init__(f'No such service "{service_name}"', *args)

    @property
    def service_name(self) -> str:
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

    Properties:
        - **option_name** (``str``, required, read-only): The name of the option.
    """

    def __init__(self, option_name: str, *args) -> None:
        self._option_name = option_name
        super().__init__(f'No such option: "{option_name}"', *args)

    @property
    def option_name(self) -> str:
        return self._option_name


class OptionExistsError(Exception):
    """
    Raised when an option already exists.

    Properties:
        - **option_name** (``str``, required, read-only): The name of the option.
    """

    def __init__(self, option_name: str, *args) -> None:
        self._option_name = option_name
        super().__init__(f'Option already exists: "{option_name}"', *args)

    @property
    def option_name(self) -> str:
        return self._option_name


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

    Properties:
        - **plugin_name** (``str``, required, read-only): The name of the plugin.
        - **plugin_package** (``str``, required, read-only): The package name of the plugin.
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
        return self._plugin_name

    @property
    def plugin_package(self) -> str:
        return self._plugin_package


class SassCompilationError(Exception):
    """
    Raised when Dart Sass compilation fails.

    Properties:
        - **stderr** (``str``, required, read-only): The stderr output from Dart Sass.
    """

    def __init__(self, stderr: str, *args: object) -> None:
        self._stderr = stderr
        super().__init__(f"SASS compilation error:\n{stderr}", *args)

    @property
    def stderr(self) -> str:
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

    Properties:
        - **monitor_id** (``int``, required, read-only): The ID of the monitor.
    """

    def __init__(self, monitor_id: int, *args: object) -> None:
        self._monitor_id = monitor_id
        super().__init__(f"No such monitor with id: {monitor_id}", *args)

    @property
    def monitor_id(self) -> int:
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

    Properties:
        - **method_name** (``str``, required, read-only): The name of the D-Bus method.
    """

    def __init__(self, method_name: str, *args: object) -> None:
        self._method_name = method_name
        super().__init__(
            f'No such registered D-Bus method with name: "{method_name}"', *args
        )

    @property
    def method_name(self) -> str:
        return self._method_name


class DBusPropertyNotFoundError(Exception):
    """
    Raised when a D-Bus property is not found or not registered.

    Properties:
        - **property_name** (``str``, required, read-only): The name of the D-Bus property.
    """

    def __init__(self, property_name: str, *args: object) -> None:
        self._property_name = property_name
        super().__init__(
            f'No such registered D-Bus property with name: "{property_name}"', *args
        )

    @property
    def property_name(self) -> str:
        return self._property_name


class DisplayNotFoundError(Exception):
    """
    Raised when the display is not found (e.g., a Wayland compositor is not running).
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "Display not found! Ensure you are running a Wayland compositor", *args
        )
