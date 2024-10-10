import os
from typing import Literal

from gi.repository import GObject  # type: ignore

from ignis.base_service import BaseService
from os import listdir

from ignis.dbus import DBusProxy
from ignis.utils import load_interface_xml, Utils


class BacklightService(BaseService):
    """
    A backlight service.
    Allows controlling device screen brightness.

    Properties:
        - **brightness** (``int``, read-write): Current brightness of your device backlight. ``-1`` if not applicable.
        - **max_brightness** (``int``, read-only): Maximum brightness allowed by your device backlight. ``-1`` if not applicable.
        - **available** (``bool``, read-only): ``True`` if your device has a controllable backlight, ``False`` if otherwise.

    **Example Usage:**

    .. code-block:: python

        from ignis.service.backlight import BacklightService

        backlight = BacklightService.get_default()

        # Getter methods
        print(backlight.get_brightness())
        print(backlight.get_max_brightness())
        print(backlight.get_available())

        # Setter method
        backlight.set_brightness(backlight.get_max_brightness())
    """

    def __init__(self):
        super().__init__()

        self._brightness: int = -1
        self._max_brightness: int = -1
        self._available = True

        # Setting initial values
        backlights = listdir("/sys/class/backlight")
        for backlight in list(backlights):
            if "backlight" in backlight:
                try:
                    self._backlight = backlight
                    self._brightness = self.__update_from_file(file="brightness", notify=False)
                    self._max_brightness = self.__update_from_file(file="max_brightness", notify=False)

                    Utils.FileMonitor(
                        path="/sys/class/backlight/" + backlight + "/brightness",
                        recursive=False,
                        # updating self._brightness and calling the signal notify::brightness
                        callback=lambda path, event_type: setattr(self, "_brightness", self.__update_from_file(file="brightness", notify=True)) if event_type == "changed" else None,
                    )

                    break
                except FileNotFoundError:
                    continue
        else:
            self._available = False

        sessionpath = self._get_session_path()
        if sessionpath == "":
            self.__dbus = None
            self._available = False
        else:
            self.__dbus = DBusProxy(
                name="org.freedesktop.login1",
                object_path=sessionpath,
                info=Utils.load_interface_xml("org.freedesktop.login1.Session"),
                interface_name="org.freedesktop.login1.Session",
                bus_type="system",
            )

    @GObject.Property(type=int)
    def max_brightness(self) -> int | None:
        return self._max_brightness

    @GObject.Property(type=int)
    def brightness(self) -> int | None:
        return self._brightness

    @brightness.setter
    def brightness(self, brightness_val: int) -> None:
        if self._available:
            self._brightness = brightness_val
            self.__set_brightness(brightness_val)

    @GObject.Property
    def available(self) -> bool:
        return self._available

    def _get_session_path(self) -> str:
        self.__session_proxy = DBusProxy(
            name="org.freedesktop.login1",
            object_path="/org/freedesktop/login1",
            info=load_interface_xml("org.freedesktop.login1.Manager"),
            interface_name="org.freedesktop.login1.Manager",
            bus_type="system",
        )

        sessionid = os.getenv("XDG_SESSION_ID", default="")
        if sessionid == "":
            return ""

        sessionpath = self.__session_proxy.GetSession("(s)", sessionid.strip() + "\x00").strip()
        return sessionpath

    def __set_brightness(self, brightness_val: int) -> None:
        if self._available and self.__dbus is not None:
            self.__dbus.SetBrightness(
                "(ssu)",
                "backlight" + "\x00",
                self._backlight.strip() + "\x00",
                brightness_val,
            )

    def __update_from_file(self, file: Literal["brightness", "max_brightness"], notify: bool) -> int:
        if self._available:
            if notify:
                self.notify("brightness")
            with open(f"/sys/class/backlight/{self._backlight}/{file}") as backlight_file:
                return int(backlight_file.read().strip())
        else:
            return -1
