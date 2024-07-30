from gi.repository import Gio, GLib, GObject
from typing import Any, List
from ignis.utils import Utils
from ignis.gobject import IgnisGObject


class DBusService(IgnisGObject):
    def __init__(
        self,
        name: str,
        object_path: str,
        info: Gio.DBusInterfaceInfo,
        on_name_acquired: callable = None,
        on_name_lost: callable = None,
    ):
        super().__init__()
        Gio.bus_own_name(
            Gio.BusType.SESSION,
            name,
            Gio.BusNameOwnerFlags.NONE,
            lambda connection, name: self.__export_object(connection, info),
            on_name_acquired,
            on_name_lost,
        )

        self._name = name
        self._object_path = object_path

        self._methods = {}
        self._properties = {}

    @GObject.Property
    def name(self) -> str:
        return self._name

    @GObject.Property
    def object_path(self) -> str:
        return self._object_path

    @GObject.Property
    def connection(self) -> Gio.DBusConnection:
        return self._connection

    @GObject.Property
    def methods(self) -> dict:
        return self._methods

    @GObject.Property
    def properties(self) -> dict:
        return self._properties

    def __export_object(self, connection, info) -> None:
        self._connection = connection
        self._connection.register_object(
            self._object_path,
            info,
            self.__handle_method_call,
            self.__handle_get_property,
            None,
        )

    def __handle_method_call(
        self,
        connection,
        sender,
        object_path,
        interface_name,
        method_name,
        params,
        invocation,
    ):
        def callback(func: callable, unpacked_params) -> None:
            result = func(invocation, *unpacked_params)
            invocation.return_value(result)

        func = self._methods.get(method_name, None)
        if func:
            # params can contain pixbuf, very large amount of data
            # and unpacking may take some time and block the main thread
            Utils.ThreadTask(
                target=params.unpack, callback=lambda result: callback(func, result)
            )

    def __handle_get_property(self, connection, sender, object_path, interface, value):
        func = self._properties.get(value, None)
        if func:
            return func()

    def register_dbus_method(self, name: str, method: callable) -> None:
        self._methods[name] = method

    def register_dbus_property(self, name: str, method: callable) -> None:
        self._properties[name] = method

    def emit_signal(self, signal_name: str, parameters: GLib.Variant = None) -> None:
        self._connection.emit_signal(
            None,
            self._object_path,
            self._name,
            signal_name,
            parameters,
        )


class DBusProxy(IgnisGObject):
    def __init__(
        self,
        name: str,
        object_path: str,
        interface_name: str,
        info: Gio.DBusInterfaceInfo,
    ):
        super().__init__()
        self._methods = []
        self._properties = []

        self._proxy = Gio.DBusProxy.new_for_bus_sync(
            Gio.BusType.SESSION,
            Gio.DBusProxyFlags.NONE,
            info,
            name,
            object_path,
            interface_name,
            None,
        )

        for i in info.methods:
            self._methods.append(i.name)

        for i in info.properties:
            self._properties.append(i.name)

    @GObject.Property
    def name(self) -> str:
        return self._proxy.get_name()

    @GObject.Property
    def object_path(self) -> str:
        return self._proxy.get_object_path()

    @GObject.Property
    def interface_name(self) -> str:
        return self._proxy.get_interface_name()

    @GObject.Property
    def connection(self) -> str:
        return self._proxy.get_connection()

    @GObject.Property
    def proxy(self) -> Gio.DBusProxy:
        return self._proxy

    @GObject.Property
    def methods(self) -> List[str]:
        return self._methods

    @GObject.Property
    def properties(self) -> List[str]:
        return self._properties

    @GObject.Property
    def has_owner(self) -> bool:
        dbus = DBusProxy(
            name="org.freedesktop.DBus",
            object_path="/org/freedesktop/DBus",
            interface_name="org.freedesktop.DBus",
            info=Utils.load_interface_xml("org.freedesktop.DBus"),
        )
        return dbus.NameHasOwner("(s)", self.name)

    def __getattr__(self, name: str) -> Any:
        if name in self.methods:
            return getattr(self._proxy, name)
        elif name in self.properties:
            return self.__get_dbus_property(name)
        else:
            return super().__getattribute__(name)

    def signal_subscribe(
        self,
        signal_name: str,
        callback: callable = None,
    ) -> None:
        self.connection.signal_subscribe(
            self.name,
            self.interface_name,
            signal_name,
            self.object_path,
            None,
            Gio.DBusSignalFlags.NONE,
            callback,
        )

    def signal_unsubscribe(self, id: int) -> None:
        self.connection.signal_unsubscribe(id)

    def __get_dbus_property(self, property_name: str) -> bool:
        try:
            return self.connection.call_sync(
                self.name,
                self.object_path,
                "org.freedesktop.DBus.Properties",
                "Get",
                GLib.Variant(
                    "(ss)",
                    (self.interface_name, property_name),
                ),
                None,
                Gio.DBusCallFlags.NONE,
                -1,
                None,
            )[0]
        except GLib.GError:
            return None

    def watch_name(
        self, on_name_appeared: callable = None, on_name_vanished: callable = None
    ) -> None:
        self._watcher = Gio.bus_watch_name(
            Gio.BusType.SESSION,
            self.name,
            Gio.BusNameWatcherFlags.NONE,
            on_name_appeared,
            on_name_vanished,
        )

    def unwatch_name(self) -> None:
        Gio.bus_unwatch_name(self._watcher)
