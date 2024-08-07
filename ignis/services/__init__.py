import importlib
from ignis.gobject import IgnisGObject


class ServiceNotFoundError(Exception):
    """
    Raised when a service with the given name is not found.
    """

    def __init__(self, service_name: str, *args: object) -> None:
        super().__init__(f'No such service "{service_name}"', *args)


class ServiceClass:
    def __init__(self) -> None:
        # modify this dict to add/remove services
        # SHORT_SERVICE_NAME: SERVICE_CLASS_NAME
        self._services = {
            "applications": "ApplicationsService",
            "audio": "AudioService",
            "fetch": "FetchService",
            "hyprland": "HyprlandService",
            "mpris": "MprisService",
            "network": "NetworkService",
            "notifications": "NotificationService",
            "options": "OptionsService",
            "recorder": "RecorderService",
            "system_tray": "SystemTrayService",
            "time": "TimeService",
            "wallpaper": "WallpaperService",
        }

    def get(self, service: str) -> IgnisGObject:
        """
        Get a service by its name.
        """
        if service in self._services:
            if not hasattr(self, f"_{service}"):
                module = importlib.import_module(f".{service}", package=__name__)
                service_class = getattr(module, self._services[service])
                setattr(self, f"_{service}", service_class())

            return getattr(self, f"_{service}")
        else:
            raise ServiceNotFoundError(service)


Service = ServiceClass()
