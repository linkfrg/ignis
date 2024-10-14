import os
from ignis.dbus import DBusProxy
from ignis.utils import Utils


def get_session_path() -> str:
    proxy = DBusProxy(
        name="org.freedesktop.login1",
        object_path="/org/freedesktop/login1",
        info=Utils.load_interface_xml("org.freedesktop.login1.Manager"),
        interface_name="org.freedesktop.login1.Manager",
        bus_type="system",
    )

    session_id = os.getenv("XDG_SESSION_ID")
    if session_id is None:
        return ""

    session_path = proxy.GetSession("(s)", session_id)
    return session_path
