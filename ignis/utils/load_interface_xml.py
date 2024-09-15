from gi.repository import Gio  # type: ignore
from .get_current_dir import get_current_dir

DBUS_DIR = get_current_dir() + "/../dbus"


def load_interface_xml(interface_name: str) -> Gio.DBusInterfaceInfo:
    """
    Load interface info from XML.
    Interfaces must be stored in the ``ignis/dbus/`` directory.

    Args:
        interface_name (``str``): The name of the interface.
    Returns:
        ``Gio.DBusInterfaceInfo``: The interface information.
    """
    file_path = f"{DBUS_DIR}/{interface_name}.xml"
    with open(file_path) as file:
        xml = file.read()
    return Gio.DBusNodeInfo.new_for_xml(xml).interfaces[0]
