class WindowNotFoundError(Exception):
    """
    Raised when a window is not found.
    """

    def __init__(self, window_name: str, *args) -> None:
        super().__init__(f'No such window: "{window_name}"', *args)


class WindowAddedError(Exception):
    """
    Raised when a window is already added to the application.
    """

    def __init__(self, window_name: str, *args) -> None:
        super().__init__(f'Window already added: "{window_name}"', *args)


class ServiceNotFoundError(Exception):
    """
    Raised when a service with the given name is not found.
    """

    def __init__(self, service_name: str, *args: object) -> None:
        super().__init__(f'No such service "{service_name}"', *args)


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


class RequestsModuleNotFoundError(Exception):
    """
    Raised when the Python requests module is not found.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "Requests module not found! To use the mpris service, install python-requests",
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

    def __init__(self, name: str, *args) -> None:
        super().__init__(f'No such option: "{name}"', *args)


class OptionExistsError(Exception):
    """
    Raised when an option already exists.
    """

    def __init__(self, name: str, *args) -> None:
        super().__init__(f'Option already exists: "{name}"', *args)


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

    def __init__(self, name: str, plugin_package: str, *args) -> None:
        super().__init__(
            f"{name} GStreamer plugin not found! To use the recorder service, install {plugin_package}",
            *args,
        )


class SassCompilationError(Exception):
    """
    Raised when Dart Sass compilation fails.
    """

    def __init__(self, stderr: str, *args: object) -> None:
        super().__init__(f"SASS compilation error:\n{stderr}", *args)


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
        super().__init__(f"No such monitor with id: {monitor_id}", *args)


class LayerShellNotSupportedError(Exception):
    """
    Raised when the Layer Shell protocol is not supported.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "zwlr_layer_shell_v1 is not supported! Ensure you are running a Wayland compositor that implements the zwlr_layer_shell_v1 protocol",
            *args,
        )
