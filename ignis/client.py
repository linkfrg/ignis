from ignis.dbus import DBusProxy
from ignis.utils import Utils


class IgnisClient:
    def __init__(self):
        self.__dbus = DBusProxy(
            name="com.github.linkfrg.ignis",
            object_path="/com/github/linkfrg/ignis",
            interface_name="com.github.linkfrg.ignis",
            info=Utils.load_interface_xml("com.github.linkfrg.ignis"),
        )

    @property
    def has_owner(self) -> bool:
        return self.__dbus.has_owner

    def __call_window_method(self, method_name: str, window_name: str) -> None:
        window_found = getattr(self.__dbus, method_name)("(s)", window_name)
        if not window_found:
            print(f"No such window: {window_name}")
            exit(1)

    def OpenWindow(self, window_name: str) -> None:
        self.__call_window_method("OpenWindow", window_name)

    def CloseWindow(self, window_name: str) -> None:
        self.__call_window_method("CloseWindow", window_name)

    def ToggleWindow(self, window_name: str) -> None:
        self.__call_window_method("ToggleWindow", window_name)

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
