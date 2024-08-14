import importlib
from ignis.gobject import IgnisGObject
from ignis.exceptions import ServiceNotFoundError


class ServiceClass:
    """
    Universal class to access services.

    .. warning::

        Do not initialize this class!
        Use the already initialized ``Service`` instance as shown below.

    .. code-block:: python

        from ignis.services import Service
        service_name = Service.get("service_name")

    """

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

        Args:
            service (``str``): A service name. It should be in ``snake_case``.

        Returns:
            IgnisGObject: The service with given name.

        Raises:
            ServiceNotFoundError: When service with given ID not found.
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
