import os
from gi.repository import GObject, Gtk, Gdk  # type: ignore
from ignis.exceptions import DisplayNotFoundError
from ignis.base_service import BaseService


class FetchService(BaseService):
    """
    A service for fetching system information.

    **Example usage**:

    .. code-block:: python

        from ignis.services.fetch import FetchService

        fetch = FetchService.get_default()

        print(fetch.os_name)
        print(fetch.hostname)
        print(fetch.kernel)
    """

    def __init__(self):
        super().__init__()
        self._os_info = self.__get_os_info()

    def __get_os_info(self) -> dict[str, str]:
        os_info = {}
        with open("/etc/os-release") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    os_info[key] = value.strip('"')

        return os_info

    @GObject.Property
    def os_name(self) -> str:
        """
        The OS name.
        """
        return self._os_info.get("NAME", "Unknown")

    @GObject.Property
    def os_id(self) -> str:
        """
        The OS ID.
        """
        return self._os_info.get("ID", "Unknown")

    @GObject.Property
    def os_build_id(self) -> str:
        """
        The OS build ID.
        """
        return self._os_info.get("BUILD_ID", "Unknown")

    @GObject.Property
    def os_ansi_color(self) -> str:
        """
        The OS ANSI color.
        """
        return self._os_info.get("ANSI_COLOR", "Unknown")

    @GObject.Property
    def os_home_url(self) -> str:
        """
        The OS homepage URL.
        """
        return self._os_info.get("HOME_URL", "Unknown")

    @GObject.Property
    def os_documentation_url(self) -> str:
        """
        The OS documentation URL.
        """
        return self._os_info.get("DOCUMENTATION_URL", "Unknown")

    @GObject.Property
    def os_support_url(self) -> str:
        """
        The OS support URL.
        """
        return self._os_info.get("SUPPORT_URL", "Unknown")

    @GObject.Property
    def os_bug_report_url(self) -> str:
        """
        The OS bug report URL.
        """
        return self._os_info.get("BUG_REPORT_URL", "Unknown")

    @GObject.Property
    def os_privacy_policy_url(self) -> str:
        """
        The OS privacy policy URL.
        """
        return self._os_info.get("PRIVACY_POLICY_URL", "Unknown")

    @GObject.Property
    def os_logo(self) -> str:
        """
        The OS logo icon name.
        """
        return self._os_info.get("LOGO", "Unknown")

    @GObject.Property
    def os_logo_dark(self) -> str:
        """
        The OS dark logo icon name.
        """
        return f"{self.os_logo}-dark"

    @GObject.Property
    def os_logo_text(self) -> str:
        """
        The OS logo with text icon name.
        """
        return f"{self.os_logo}-text"

    @GObject.Property
    def os_logo_text_dark(self) -> str:
        """
        The OS dark logo with text icon name.
        """
        return f"{self.os_logo}-text-dark"

    @GObject.Property
    def session_type(self) -> str | None:
        """
        The current session type (wayland/x11).
        """
        return os.environ.get("XDG_SESSION_TYPE")

    @GObject.Property
    def current_desktop(self) -> str | None:
        """
        The current desktop environment.
        """
        return os.environ.get("XDG_CURRENT_DESKTOP")

    @GObject.Property
    def hostname(self) -> str:
        """
        The hostname of this machine.
        """
        with open("/etc/hostname") as file:
            data = file.read()
        return data

    @GObject.Property
    def kernel(self) -> str:
        """
        Kernel version.
        """
        return os.uname().release

    @GObject.Property
    def uptime(self) -> tuple[int, int, int, int]:
        """
        Current uptime, (days, hours, minutes, seconds).

        You can use :class:`~ignis.utils.Utils.Poll` to get the current uptime every minute or second.
        """
        with open("/proc/uptime") as f:
            uptime_seconds = float(f.readline().split()[0])

        uptime_minutes, seconds = divmod(uptime_seconds, 60)
        uptime_hours, minutes = divmod(uptime_minutes, 60)
        days, hours = divmod(uptime_hours, 24)

        return int(days), int(hours), int(minutes), int(seconds)

    @GObject.Property
    def cpu(self) -> str:
        """
        CPU model.
        """
        cpu_name = "Unknown"
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    cpu_name = line.split(":")[1].strip()
                    break
        return cpu_name

    @GObject.Property
    def mem_info(self) -> dict[str, int]:
        """
        Dictionary with all information about RAM.
        """
        mem_info = {}
        with open("/proc/meminfo") as file:
            for line in file:
                key, value = line.split(":")
                value = value.replace("kB", "")
                value = value.replace(" ", "")
                mem_info[key.strip()] = int(value)
        return mem_info

    @GObject.Property
    def mem_total(self) -> int:
        """
        Total amount of RAM.
        """
        return self.mem_info.get("MemTotal", None)

    @GObject.Property
    def mem_available(self) -> int:
        """
        Available amount of RAM.
        """
        return self.mem_info.get("MemAvailable", None)

    @GObject.Property
    def mem_used(self) -> int:
        """
        Vendor of the motherboard.
        """
        return self.mem_total - self.mem_available

    @GObject.Property
    def board_vendor(self) -> str:
        """
        Motherboard name.
        """
        with open("/sys/devices/virtual/dmi/id/board_vendor") as file:
            data = file.read()

        return data.strip()

    @GObject.Property
    def board_name(self) -> str:
        """
        BIOS/UEFI version.
        """
        with open("/sys/devices/virtual/dmi/id/board_name") as file:
            data = file.read()

        return data.strip()

    @GObject.Property
    def bios_version(self) -> str:
        with open("/sys/devices/virtual/dmi/id/bios_version") as file:
            data = file.read()

        return data.strip()

    @GObject.Property
    def gtk_theme(self) -> str | None:
        """
        Current GTK theme.
        """
        settings = Gtk.Settings.get_default()
        if not settings:
            return None

        return settings.get_property("gtk-theme-name")

    @GObject.Property
    def icon_theme(self) -> str | None:
        """
        Current icon theme.
        """
        display = Gdk.Display.get_default()
        if not display:
            raise DisplayNotFoundError()

        return Gtk.IconTheme.get_for_display(display).get_theme_name()
