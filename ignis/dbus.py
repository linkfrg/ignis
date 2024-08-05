from gi.repository import Gio, GLib, GObject
from typing import Any, List
from ignis.utils import Utils
from ignis.gobject import IgnisGObject


class DBusService(IgnisGObject):
    """
    Class to help create DBus services.

    Parameters:
        name (``str``): The well-known name to own.
        object_path (``str``): An object path.
        info (`Gio.DBusInterfaceInfo <https://lazka.github.io/pgi-docs/Gio-2.0/classes/DBusInterfaceInfo.html>`_): A ``Gio.DBusInterfaceInfo`` instance. You can get it from XML using :class:`~ignis.utils.Utils.load_interface_xml`.
        on_name_acquired (``callable``, optional): Function to call when ``name`` is acquired.
        on_name_acquired (``callable``, optional): Function to call when ``name`` is lost.

    Properties:
        - **name** (``str``, read-only): The well-known name to own.
        - **object_path** (``str``, read-only): An object path.
        - **connection** (`Gio.DBusConnection <https://lazka.github.io/pgi-docs/Gio-2.0/classes/DBusConnection.html>`_, read-only): The ``Gio.DBusConnection`` instance.
        - **methods** (``dict``, read-only): The dictionary of registred DBus methods. See :func:`~ignis.dbus.DBusService.register_dbus_method`.
        - **properties** (``dict``, read-only): The dictionary of registred DBus properties. See :func:`~ignis.dbus.DBusService.register_dbus_property`.

    DBus methods:
        - must accept `Gio.DBusMethodInvocation <https://lazka.github.io/pgi-docs/index.html#Gio-2.0/classes/DBusMethodInvocation.html>`_ as the first argument.
        - must accept all other arguments, typical for this method (specified by interface info).
        - must return `GLib.Variant <https://lazka.github.io/pgi-docs/index.html#GLib-2.0/classes/Variant.html>`_ or ``None``, specified by interface info.

    DBus properties:
        - must return `GLib.Variant <https://lazka.github.io/pgi-docs/index.html#GLib-2.0/classes/Variant.html>`_, specified by interface info.

    .. code-block:: python

        from gi.repository import Gio, GLib
        from ignis.dbus import DBusService

        def _MyMethod(invocation: Gio.DBusMethodInvocation, prop1: str, prop2: str, *args) -> GLib.Variant:
            print("do something")
            return GLib.Variant("(is)", (42, "hello"))

        def _MyProperty() -> GLib.Variant:
            return GLib.Variant("(b)", (False,))

        dbus = DBusService(...)
        dbus.register_dbus_method("MyMethod", _MyMethod)
        dbus.register_dbus_property("MyProperty", _MyProperty)
    """

    def __init__(
        self,
        name: str,
        object_path: str,
        info: Gio.DBusInterfaceInfo,
        on_name_acquired: callable = None,
        on_name_lost: callable = None,
    ):
        super().__init__()
        self.__id = Gio.bus_own_name(
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

    def __export_object(self, connection: Gio.DBusConnection, info: Gio.DBusInterfaceInfo) -> None:
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
        connection: Gio.DBusConnection,
        sender: str,
        object_path: str,
        interface_name: str,
        method_name: str,
        params: GLib.Variant,
        invocation: Gio.DBusMethodInvocation,
    ) -> None:
        def callback(func: callable, unpacked_params) -> None:
            result = func(invocation, *unpacked_params)
            invocation.return_value(result)

        func = self._methods.get(method_name, None)
        if func:
            # params can contain pixbuf, very large amount of data
            # and unpacking may take some time and block the main thread
            # so we unpack in another thread, and call DBus method when unpacking is finished
            Utils.ThreadTask(
                target=params.unpack, callback=lambda result: callback(func, result)
            )

    def __handle_get_property(self, connection: Gio.DBusConnection, sender: str, object_path: str, interface: str, value: str) -> GLib.Variant:
        func = self._properties.get(value, None)
        if func:
            return func()

    def register_dbus_method(self, name: str, method: callable) -> None:
        """
        Register DBus method for this service.

        Args:
            name (``str``): The name of the method to register.
            method (``callable``): A function to call when method is called (from DBus).
        """
        self._methods[name] = method

    def register_dbus_property(self, name: str, method: callable) -> None:
        """
        Register DBus property for this service.

        Args:
            name (``str``): The name of the property to register.
            method (``callable``): A function to call when property is getted (from DBus).
        """
        self._properties[name] = method

    def emit_signal(self, signal_name: str, parameters: GLib.Variant = None) -> None:
        """
        Emit DBus signal on self ``name`` and ``object_path``.

        Args:
            signal_name (``str``): The signal name to emit.
            parameters (`GLib.Variant <https://lazka.github.io/pgi-docs/index.html#GLib-2.0/classes/Variant.html>`_, optional): The ``GLib.Variant`` containing paramaters to pass with signal.

        """
        self._connection.emit_signal(
            None,
            self._object_path,
            self._name,
            signal_name,
            parameters,
        )

    def unown_name(self) -> None:
        """
        Unown name.
        """
        Gio.bus_unown_name(self.__id)


class DBusProxy(IgnisGObject):
    """
    Class to help to interact with D-Bus services (create D-Bus proxy).
    Unlike `Gio.DBusProxy <https://lazka.github.io/pgi-docs/index.html#Gio-2.0/classes/DBusProxy.html>`_ also provides comfortable pythonic property getting.

    Parameters:
        name (``str``): A bus name (well-known or unique).
        object_path (``str``): An object path.
        interface_name (``str``): A D-Bus interface name.
        info (`Gio.DBusInterfaceInfo <https://lazka.github.io/pgi-docs/Gio-2.0/classes/DBusInterfaceInfo.html>`_): A ``Gio.DBusInterfaceInfo`` instance. You can get it from XML using :class:`~ignis.utils.Utils.load_interface_xml`.

    Properties:
        - **name** (``str``, read-only): A bus name (well-known or unique).
        - **object_path** (``str``, read-only): An object path.
        - **interface_name** (``str``, read-only): A D-Bus interface name.
        - **proxy** (`Gio.DBusProxy <https://lazka.github.io/pgi-docs/index.html#Gio-2.0/classes/DBusProxy.html>`_, read-only): The ``Gio.DBusProxy`` instance.
        - **methods** (``List[str]``, read-only): A list of methods exposed by DBus service.
        - **properties** (``List[str]``, read-only): A list of properties exposed by DBus service.
        - **has_owner** (``bool``, read-only): Whether ``name`` has owner.

    To call D-Bus method use the standart pythonic way.
    The first argument always needs to be the DBus signature tuple of the method call.
    Next arguments must match provided D-Bus signature.
    If D-Bus method does not accept any arguments, do not pass arguments.

    .. code-block:: python

        from ignis.dbus import DBusProxy
        proxy = DBusProxy(...)
        proxy.MyMethod("(is)", 42, "hello")

    To get D-Bus property also use the standart pythonic way.

    .. code-block:: python

        from ignis.dbus import DBusProxy
        proxy = DBusProxy(...)
        value = proxy.MyValue
        print(value)
    """
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
    ) -> int:
        """
        Subscribe to D-Bus signal.

        Args:
            signal_name (``str``): The signal name to subscribe.
            callback (``callable``, optional): A function to call when signal is emitted.
        Returns:
            ``int``: a subscription ID that can be used with :func:`~ignis.dbus.DBusProxy.signal_unsubscribe`
        """
        return self.connection.signal_subscribe(
            self.name,
            self.interface_name,
            signal_name,
            self.object_path,
            None,
            Gio.DBusSignalFlags.NONE,
            callback,
        )

    def signal_unsubscribe(self, id: int) -> None:
        """
        Unsubscribe from D-Bus signal.

        Args:
            id (``int``): The ID of the subscription.
        """
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
        """
        Watch ``name``.

        Args:
            on_name_appeared (``callable``, optional): A function to call when ``name`` appeared.
            on_name_vanished (``callable``, optional): A function to call when ``name`` vanished.
        """
        self._watcher = Gio.bus_watch_name(
            Gio.BusType.SESSION,
            self.name,
            Gio.BusNameWatcherFlags.NONE,
            on_name_appeared,
            on_name_vanished,
        )

    def unwatch_name(self) -> None:
        """
        Unwatch name.
        """
        Gio.bus_unwatch_name(self._watcher)
