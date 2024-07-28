import os
from gi.repository import Gio

DBUS_DIR = f"{os.path.dirname(os.path.abspath(__file__))}/../dbus"


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
    with open(file_path, "r") as file:
        xml = file.read()
    return Gio.DBusNodeInfo.new_for_xml(xml).interfaces[0]
