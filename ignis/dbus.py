from gi.repository import Gio, GLib, GObject  # type: ignore
from typing import Any, Callable
from ignis.utils import Utils
from ignis.gobject import IgnisGObject
from ignis.exceptions import DBusMethodNotFoundError, DBusPropertyNotFoundError
from typing import Literal, Union

BUS_TYPE = {"session": Gio.BusType.SESSION, "system": Gio.BusType.SYSTEM}


class DBusService(IgnisGObject):
    """
    A class that helps create a D-Bus service.

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
        on_name_acquired: Callable | None = None,
        on_name_lost: Callable | None = None,
    ):
        super().__init__()

        self._name = name
        self._object_path = object_path
        self._info = info
        self._on_name_acquired = on_name_acquired
        self._on_name_lost = on_name_lost

        self._methods: dict[str, Callable] = {}
        self._properties: dict[str, Callable] = {}

        self._id = Gio.bus_own_name(
            Gio.BusType.SESSION,
            name,
            Gio.BusNameOwnerFlags.NONE,
            self.__export_object,
            self._on_name_acquired,
            self._on_name_lost,
        )

    @GObject.Property
    def name(self) -> str:
        """
        - required, read-only

        The well-known name to own.
        """
        return self._name

    @GObject.Property
    def object_path(self) -> str:
        """
        - required, read-only

        An object path.
        """
        return self._object_path

    @GObject.Property
    def info(self) -> Gio.DBusInterfaceInfo:
        """
        - required, read-only

        An instance of :class:`Gio.DBusInterfaceInfo`

        You can get it from XML using :func:`~ignis.utils.Utils.load_interface_xml`.
        """
        return self._info

    @GObject.Property
    def on_name_acquired(self) -> Callable:
        """
        - optional, read-write

        The function to call when ``name`` is acquired.
        """
        return self._on_name_acquired

    @on_name_acquired.setter
    def on_name_acquired(self, value: Callable) -> None:
        self._on_name_acquired = value

    @GObject.Property
    def on_name_lost(self) -> Callable:
        """
        - optional, read-write

        The function to call when ``name`` is lost.
        """
        return self._on_name_lost

    @on_name_lost.setter
    def on_name_lost(self, value: Callable) -> None:
        self._on_name_lost = value

    @GObject.Property
    def connection(self) -> Gio.DBusConnection:
        """
        - not argument, read-only

        The instance of :class:`Gio.DBusConnection` for this service.
        """
        return self._connection

    @GObject.Property
    def methods(self) -> dict[str, Callable]:
        """
        - not argument, read-only

        The dictionary of registred DBus methods. See :func:`~ignis.dbus.DBusService.register_dbus_method`.
        """
        return self._methods

    @GObject.Property
    def properties(self) -> dict[str, Callable]:
        """
        - not argument, read-only

        The dictionary of registred DBus properties. See :func:`~ignis.dbus.DBusService.register_dbus_property`.
        """
        return self._properties

    def __export_object(self, connection: Gio.DBusConnection, name: str) -> None:
        self._connection = connection
        self._connection.register_object(
            self._object_path,
            self._info,
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
        def callback(func: Callable, unpacked_params) -> None:
            result = func(invocation, *unpacked_params)
            invocation.return_value(result)

        func = self._methods.get(method_name, None)
        if not func:
            raise DBusMethodNotFoundError(method_name)

        # params can contain pixbuf, very large amount of data
        # and unpacking may take some time and block the main thread
        # so we unpack in another thread, and call DBus method when unpacking is finished
        Utils.ThreadTask(
            target=params.unpack, callback=lambda result: callback(func, result)
        ).run()

    def __handle_get_property(
        self,
        connection: Gio.DBusConnection,
        sender: str,
        object_path: str,
        interface: str,
        value: str,
    ) -> GLib.Variant:
        func = self._properties.get(value, None)
        if not func:
            raise DBusPropertyNotFoundError(value)

        return func()

    def register_dbus_method(self, name: str, method: Callable) -> None:
        """
        Register a D-Bus method for this service.

        Args:
            name: The name of the method to register.
            method: A function to call when the method is invoked (from D-Bus).

        DBus methods:
            - Must accept :class:`Gio.DBusMethodInvocation` as the first argument.
            - Must accept all other arguments typical for this method (specified by interface info).
            - Must return :class:`GLib.Variant` or ``None``, as specified by interface info.
        """
        self._methods[name] = method

    def register_dbus_property(self, name: str, method: Callable) -> None:
        """
        Register D-Bus property for this service.

        Args:
            name: The name of the property to register.
            method: A function to call when the property is accessed (from DBus).

        DBus properties:
            - Must return :class:`GLib.Variant`, as specified by interface info.
        """
        self._properties[name] = method

    def emit_signal(
        self, signal_name: str, parameters: Union[GLib.Variant, None] = None
    ) -> None:
        """
        Emit a D-Bus signal on this service.

        Args:
            signal_name: The name of the signal to emit.
            parameters: The :class:`GLib.Variant` containing paramaters to pass with the signal.
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
        Release ownership of the name.
        """
        Gio.bus_unown_name(self._id)


class DBusProxy(IgnisGObject):
    """
    A class to interact with D-Bus services (create a D-Bus proxy).
    Unlike :class:`Gio.DBusProxy>`,
    this class also provides convenient pythonic property access.

    To call a D-Bus method, use the standart pythonic way.
    The first argument always needs to be the DBus signature tuple of the method call.
    Next arguments must match the provided D-Bus signature.
    If the D-Bus method does not accept any arguments, do not pass them.

    .. code-block:: python

        from ignis.dbus import DBusProxy
        proxy = DBusProxy(...)
        result = proxy.MyMethod("(is)", 42, "hello")
        print(result)

    To get a D-Bus property:

    .. code-block:: python

        from ignis.dbus import DBusProxy
        proxy = DBusProxy(...)
        print(proxy.MyValue)

    To set a D-Bus property:

    .. code-block:: python

        from ignis.dbus import DBusProxy
        proxy = DBusProxy(...)
        # pass GLib.Variant as new property value
        proxy.MyValue = GLib.Variant("s", "Hello world!")
    """

    def __init__(
        self,
        name: str,
        object_path: str,
        interface_name: str,
        info: Gio.DBusInterfaceInfo,
        bus_type: Literal["session", "system"] = "session",
    ):
        super().__init__()
        self._name = name
        self._object_path = object_path
        self._interface_name = interface_name
        self._info = info
        self._bus_type = bus_type

        self._methods: list[str] = []
        self._properties: list[str] = []

        self._proxy = Gio.DBusProxy.new_for_bus_sync(
            BUS_TYPE[bus_type],
            Gio.DBusProxyFlags.NONE,
            info,
            name,
            object_path,
            interface_name,
            None,
        )

        for i in info.methods:
            self._methods.append(i.name)

        for i in info.properties:  # type: ignore
            self._properties.append(i.name)

    @GObject.Property
    def name(self) -> str:
        """
        - required, read-only

        A bus name (well-known or unique).
        """
        return self._name

    @GObject.Property
    def object_path(self) -> str:
        """
        - required, read-only

        An object path.
        """
        return self._object_path

    @GObject.Property
    def interface_name(self) -> str:
        """
        - required, read-only

        A D-Bus interface name.
        """
        return self._interface_name

    @GObject.Property
    def info(self) -> Gio.DBusInterfaceInfo:
        """
        - required, read-only

        A :class:`Gio.DBusInterfaceInfo` instance.

        You can get it from XML using :class:`~ignis.utils.Utils.load_interface_xml`.
        """
        return self._info

    @GObject.Property
    def bus_type(self) -> Literal["session", "system"]:
        """
        - optional, read-only

        The type of the bus.

        Default: ``session``.
        """
        return self._bus_type

    @GObject.Property
    def proxy(self) -> Gio.DBusProxy:
        """
        - not argument, read-only

        The :class:`Gio.DBusProxy` instance.
        """
        return self._proxy

    @GObject.Property
    def connection(self) -> Gio.DBusConnection:
        """
        - not argument, read-only

        The instance of :class:`Gio.DBusConnection` for this proxy.
        """
        return self._proxy.get_connection()

    @GObject.Property
    def methods(self) -> list[str]:
        """
        - not argument, read-only

        A list of methods exposed by D-Bus service.
        """
        return self._methods

    @GObject.Property
    def properties(self) -> list[str]:
        """
        - not argument, read-only

        A list of properties exposed by D-Bus service.
        """
        return self._properties

    @GObject.Property
    def has_owner(self) -> bool:
        """
        - not argument, read-only

        Whether the ``name`` has an owner.
        """
        dbus = DBusProxy(
            name="org.freedesktop.DBus",
            object_path="/org/freedesktop/DBus",
            interface_name="org.freedesktop.DBus",
            info=Utils.load_interface_xml("org.freedesktop.DBus"),
            bus_type=self._bus_type,
        )
        return dbus.NameHasOwner("(s)", self.name)

    def __getattr__(self, name: str) -> Any:
        if name in self.methods:
            return getattr(self._proxy, name)
        elif name in self.properties:
            return self.__get_dbus_property(name)
        else:
            return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__dict__.get("_properties", {}):  # avoid recursion
            self.__set_dbus_property(name, value)
        else:
            return super().__setattr__(name, value)

    def signal_subscribe(
        self,
        signal_name: str,
        callback: Callable | None = None,
    ) -> int:
        """
        Subscribe to D-Bus signal.

        Args:
            signal_name: The signal name to subscribe.
            callback: A function to call when signal is emitted.
        Returns:
            A subscription ID that can be used with :func:`~ignis.dbus.DBusProxy.signal_unsubscribe`
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
            id: The ID of the subscription.
        """
        self.connection.signal_unsubscribe(id)

    def __get_dbus_property(self, property_name: str) -> Any:
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
        except GLib.GError:  # type: ignore
            return None

    def __set_dbus_property(self, property_name: str, value: GLib.Variant) -> None:
        self.connection.call_sync(
            self.name,
            self.object_path,
            "org.freedesktop.DBus.Properties",
            "Set",
            GLib.Variant(
                "(ssv)",
                (self.interface_name, property_name, value),
            ),
            None,
            Gio.DBusCallFlags.NONE,
            -1,
            None,
        )

    def watch_name(
        self,
        on_name_appeared: Callable | None = None,
        on_name_vanished: Callable | None = None,
    ) -> None:
        """
        Watch ``name``.

        Args:
            on_name_appeared: A function to call when ``name`` appeared.
            on_name_vanished: A function to call when ``name`` vanished.
        """
        self._watcher = Gio.bus_watch_name(
            BUS_TYPE[self._bus_type],
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
