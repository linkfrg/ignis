from subprocess import CalledProcessError

from gi.repository import GLib, GObject  # type: ignore
from loguru import logger

from ignis.base_service import BaseService
from os import listdir

from ignis.dbus import DBusProxy
from ignis.utils import load_interface_xml, exec_sh, Utils
from gi.repository import Gio


class BacklightService(BaseService):
    def __init__(self):
        super().__init__()

        self._brightness: int | None = None
        self._max_brightness: int | None = None
        self._enabled = True

        # Setting initial values
        backlights = listdir("/sys/class/backlight")
        for backlight in list(backlights):
            try:
                with open("/sys/class/backlight/" + backlight + "/brightness", "r") as brightness_file:
                    self._brightness = int(brightness_file.read().strip())
                with open("/sys/class/backlight/" + backlight + "/max_brightness", 'r') as max_brightness_file:
                    self._max_brightness = int(max_brightness_file.read().strip())
                self.__backlight = backlight
                break
            except:
                continue
        else:
            self._enabled = False
            logger.warning("Backlight not found. Brightness support disabled.")

        self.__dbus = DBusProxy(
            name="org.freedesktop.login1",
            object_path=self._get_session_path(),
            info=Utils.load_interface_xml("org.freedesktop.login1.Session"),
            interface_name="org.freedesktop.login1.Session",
            type=Gio.BusType.SYSTEM
        )

    @GObject.Property(type=int)
    def max_brightness(self) -> int | None:
        return self._max_brightness

    @GObject.Property(type=int)
    def brightness(self) -> int | None:
        return self._brightness

    @brightness.setter
    def brightness(self, brightness_val: int) -> None:
        self._brightness = brightness_val
        self.__set_brightness(brightness_val)


    def _get_session_path(self):
        self.__session_proxy = DBusProxy(
            name="org.freedesktop.login1",
            object_path="/org/freedesktop/login1",
            info=load_interface_xml("org.freedesktop.login1.Manager"),
            interface_name="org.freedesktop.login1.Manager",
            type=Gio.BusType.SYSTEM
        )

        sessionid = exec_sh("echo $XDG_SESSION_ID")
        try:
            sessionid.check_returncode()
            sessionid = sessionid.stdout
        except CalledProcessError:
            logger.error("Failed to get session id")
            return

        sessionpath = self.__session_proxy.GetSession('(s)', sessionid.strip() + '\x00').strip()
        return sessionpath

    def __set_brightness(self, brightness_val: int) -> None:
        if self._enabled:
            self.__dbus.SetBrightness("(ssu)", "backlight" + "\x00", self.__backlight.strip() + "\x00", brightness_val)
            logger.info(f"set brightness to: {brightness_val}")

