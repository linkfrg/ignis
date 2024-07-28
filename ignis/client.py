from ignis.dbus import DBusProxy
from ignis.utils import Utils

class IgnisClient:
    def __init__(self):
        self.__dbus = DBusProxy(
            name="com.github.linkfrg.ignis",
            object_path="/com/github/linkfrg/ignis",
            interface_name="com.github.linkfrg.ignis",
            info=Utils.load_interface_xml("com.github.linkfrg.ignis")
        )

    @property
    def has_owner(self) -> bool:
        return self.__dbus.has_owner

    def OpenWindow(self, window: str) -> None:
        self.__dbus.OpenWindow("(s)", window)

    def CloseWindow(self, window: str) -> None:
        self.__dbus.CloseWindow("(s)", window)

    def ToggleWindow(self, window: str) -> None:
        self.__dbus.ToggleWindow("(s)", window)

    def ListWindows(self) -> None:
        response = self.__dbus.ListWindows()
        print("\n".join(response))

    def Quit(self) -> None:
        self.__dbus.Quit()

    def Inspector(self) -> None:
        self.__dbus.Inspector()

    def RunPython(self, code: str) -> None:
        self.__dbus.RunPython("(s)", code)

    def RunFile(self, path: str) -> None:
        self.__dbus.RunFile("(s)", path)

    def Reload(self) -> None:
        self.__dbus.Reload()
