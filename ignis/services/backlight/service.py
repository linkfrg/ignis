from subprocess import CalledProcessError

from gi.repository import GObject, Gio  # type: ignore
from loguru import logger

from ignis.base_service import BaseService
from os import listdir

from ignis.dbus import DBusProxy
from ignis.utils import load_interface_xml, exec_sh, Utils


class BacklightService(BaseService):
    def __init__(self):
        super().__init__()

        self._brightness: int = -1
        self._max_brightness: int = -1
        self._active = True

        # Setting initial values
        backlights = listdir("/sys/class/backlight")
        for backlight in list(backlights):
            if "backlight" in backlight:
                try:
                    with open(
                        "/sys/class/backlight/" + backlight + "/brightness"
                    ) as brightness_file:
                        self._brightness = int(brightness_file.read().strip())
                    with open(
                        "/sys/class/backlight/" + backlight + "/max_brightness"
                    ) as max_brightness_file:
                        self._max_brightness = int(max_brightness_file.read().strip())
                    self.__backlight = backlight

                    Utils.FileMonitor(
                        path="/sys/class/backlight/" + backlight + "/brightness",
                        recursive=False,
                        callback=lambda path, event_type: self.__update_brightness()
                        if event_type == "changed"
                        else None,
                    )

                    break
                except FileNotFoundError:
                    continue
        else:
            self._active = False
            logger.warning("Backlight not found. Brightness support disabled.")

        sessionpath = self._get_session_path()
        if sessionpath == "":
            self.__dbus = None
            self._active = False
        else:
            self.__dbus = DBusProxy(
                name="org.freedesktop.login1",
                object_path=self._get_session_path(),
                info=Utils.load_interface_xml("org.freedesktop.login1.Session"),
                interface_name="org.freedesktop.login1.Session",
                bus_type="system"
            )

    @GObject.Property(type=int)
    def max_brightness(self) -> int | None:
        return self._max_brightness

    @GObject.Property(type=int)
    def brightness(self) -> int | None:
        return self._brightness

    @brightness.setter
    def brightness(self, brightness_val: int) -> None:
        if self._active:
            self._brightness = brightness_val
            self.__set_brightness(brightness_val)

    @GObject.Property
    def active(self) -> bool:
        return self._active

    def _get_session_path(self) -> str:
        self.__session_proxy = DBusProxy(
            name="org.freedesktop.login1",
            object_path="/org/freedesktop/login1",
            info=load_interface_xml("org.freedesktop.login1.Manager"),
            interface_name="org.freedesktop.login1.Manager",
            bus_type="system"
        )

        sessionidcmd = exec_sh("echo $XDG_SESSION_ID")
        try:
            sessionidcmd.check_returncode()
            sessionid = str(sessionidcmd.stdout)
        except CalledProcessError:
            logger.error("Failed to get session id.")
            return ""

        sessionpath = self.__session_proxy.GetSession(
            "(s)", sessionid.strip() + "\x00"
        ).strip()
        return sessionpath

    def __set_brightness(self, brightness_val: int) -> None:
        if self._active and self.__dbus is not None:
            self.__dbus.SetBrightness(
                "(ssu)",
                "backlight" + "\x00",
                self.__backlight.strip() + "\x00",
                brightness_val,
            )

    def __update_brightness(self) -> None:
        with open("/sys/class/backlight/" + self.__backlight + "/brightness") as file:
            self._brightness = int(file.read().strip())
            self.notify("brightness")
