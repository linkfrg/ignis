from gi.repository import GLib  # type: ignore
from ignis.dbus import DBusProxy
from ignis.utils import Utils
from typing import Callable


class SessionManager:
    """
    :meta private:

    Internal class for interacting with the XDG Desktop Portal to request a screencast.
    """

    def __init__(self) -> None:
        self.__dbus = DBusProxy(
            name="org.freedesktop.portal.Desktop",
            object_path="/org/freedesktop/portal/desktop",
            interface_name="org.freedesktop.portal.ScreenCast",
            info=Utils.load_interface_xml("org.freedesktop.portal.ScreenCast"),
        )

        self._session_token_counter: int = 0
        self._request_token_counter: int = 0
        self._callback: Callable | None = None
        self._calback_args: tuple = ()
        self._session: str | None = None

        self._sender_name = (
            self.__dbus.connection.get_unique_name().replace(".", "_").replace(":", "")
        )

    def start_session(self, callback: Callable, *args) -> None:
        self._callback = callback
        self._calback_args = args
        self.__create_session()

    def __create_session(self) -> None:
        request_token = self.__request_response(self.__on_create_session_response)
        self._session_token_counter += 1
        session_token = f"u{self._session_token_counter}"
        self.__dbus.CreateSession(
            "(a{sv})",
            {
                "session_handle_token": GLib.Variant("s", session_token),
                "handle_token": GLib.Variant("s", request_token),
            },
        )

    def __request_response(self, callback: Callable) -> str:
        self._request_token_counter += 1
        request_token = f"u{self._request_token_counter}"
        request_path = f"/org/freedesktop/portal/desktop/request/{self._sender_name}/{request_token}"
        request_proxy = DBusProxy(
            name="org.freedesktop.portal.Desktop",
            object_path=request_path,
            interface_name="org.freedesktop.portal.Request",
            info=Utils.load_interface_xml("org.freedesktop.portal.Request"),
        )

        request_proxy.signal_subscribe(
            signal_name="Response",
            callback=callback,
        )

        return request_token

    def __on_create_session_response(self, *args):
        response = args[5]
        response_code = response[0]
        self._session = response[1]["session_handle"]

        if response_code != 0:
            return

        request_token = self.__request_response(self.__on_select_sources_response)

        self.__dbus.SelectSources(
            "(oa{sv})",
            self._session,
            {
                "handle_token": GLib.Variant("s", request_token),
                "multiple": GLib.Variant("b", False),
                "types": GLib.Variant("u", 1 | 2),
            },
        )

    def __on_select_sources_response(self, *args) -> None:
        response_code = args[5][0]

        if response_code != 0:
            return

        request_token = self.__request_response(self.__on_start_response)
        self.__dbus.Start(
            "(osa{sv})",
            self._session,
            "",
            {
                "handle_token": GLib.Variant("s", request_token),
            },
        )

    def __on_start_response(self, *args):
        results = args[5][1]
        response_code = args[5][0]

        if response_code != 0:
            return

        for node_id, _stream_properties in results["streams"]:
            self.__run_callback(node_id)

    def __run_callback(self, node_id: int) -> None:
        if self._callback:
            self._callback(node_id, *self._calback_args)
