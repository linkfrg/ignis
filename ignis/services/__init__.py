import importlib
from ignis.gobject import IgnisGObject


class ServiceNotFoundError(Exception):
    def __init__(self, service_name: str, *args: object) -> None:
        super().__init__(f'No such service "{service_name}"', *args)


class ServiceClass:
    def __init__(self) -> None:
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
        if service in self._services:
            if not hasattr(self, f"_{service}"):
                module = importlib.import_module(f".{service}", package=__name__)
                service_class = getattr(module, self._services[service])
                setattr(self, f"_{service}", service_class())

            return getattr(self, f"_{service}")
        else:
            raise ServiceNotFoundError(service)


Service = ServiceClass()
