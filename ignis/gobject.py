import sys
from types import UnionType
from gi.repository import GObject, GLib  # type: ignore
from typing import Any, Literal, get_args, get_origin
from collections.abc import Callable


class Binding(GObject.Object):
    """
    An object that describe binding.
    """

    def __init__(
        self,
        target: GObject.Object,
        target_properties: list[str],
        transform: Callable | None = None,
    ):
        self._target = target
        self._target_properties = target_properties
        self._transform = transform
        super().__init__()

    @GObject.Property
    def target(self) -> GObject.Object:
        """
        - required, read-only

        The target GObject.
        """
        return self._target

    @GObject.Property
    def target_properties(self) -> list[str]:
        """
        - required, read-only

        The properties on the target GObject to bind.
        """
        return self._target_properties

    @GObject.Property
    def transform(self) -> Callable | None:
        """
        - required, read-only

        The function that accepts a new property value and returns the processed value.
        """
        return self._transform


class IgnisGObject(GObject.Object):
    """
    Bases: :class:`GObject.Object`

    A base class for all services and widgets (and some utils).
    Mainly, it is the same GObject.Object, but with some improvements.

    1. It provides support for :class:`~ignis.gobject.Binding`.
    2. It offers easier control over properties (without the need for the ``.props`` attribute).

    """

    def __init__(self, **kwargs):
        super().__init__()
        for key in kwargs.keys():
            self.set_property(key, kwargs[key])

    def emit(self, signal_name: str, *args):
        """
        :meta private:
        """
        # Same ``emit``, but with ``GLib.idle_add``, to avoid possible segmentation faults due to multithreading.
        GLib.idle_add(super().emit, signal_name, *args)

    def notify(self, property_name: str):
        """
        :meta private:
        """
        # Same ``notify``, but with ``GLib.idle_add``, to avoid possible segmentation faults due to multithreading.
        GLib.idle_add(super().notify, property_name)

    def notify_all(self, without: list[str] | str | None = None) -> None:
        """
        Notify all properties.

        Args:
            without: A property or a list of properties that will not be notified.
        """
        for i in self.list_properties():
            if without:
                if i.name in without:
                    continue
            self.notify(i.name)

    def notify_list(self, *args) -> None:
        """
        Notify list of properties.
        You can pass unlimited number of property names as arguments.
        """
        for i in args:
            self.notify(i)

    def set_property(self, property_name: str, value: Any) -> None:
        """
        :meta private:
        """
        if isinstance(value, Binding):
            self.bind_property2(
                source_property=property_name,
                target=value.target,
                target_properties=value.target_properties,
                transform=value.transform,
            )
        else:
            super().set_property(property_name, value)

    def bind_property2(
        self,
        source_property: str,
        target: GObject.Object,
        target_properties: list[str],
        transform: Callable | None = None,
    ) -> None:
        """
        Bind ``source_property`` on ``self`` with ``target_properties`` on ``target``.

        Args:
            source_property: The property on ``self`` to bind.
            target: the target ``GObject.Object``.
            target_properties: the properties on ``target`` to bind.
            transform: The function that accepts a new property value and returns the processed value.
        """

        def callback(*args):
            values = [
                target.get_property(target_property.replace("-", "_"))
                for target_property in target_properties
            ]

            if transform:
                value = transform(*values)
            else:
                if len(values) != 1:
                    raise IndexError("No transform function on multiple binding")
                value = values[0]

            self.set_property(source_property, value)

        for target_property in target_properties:
            target.connect(f"notify::{target_property.replace('_', '-')}", callback)

        callback()

    def bind(self, property_name: str, transform: Callable | None = None) -> Binding:
        """
        Creates ``Binding`` from property name on ``self``.

        Args:
            property_name: Property name of ``self``.
            transform: The function that accepts a new property value and returns the processed value.
        Returns:
            :class:`~ignis.gobject.Binding`
        """
        return Binding(self, [property_name], transform)

    def bind_many(self, property_names: list[str], transform: Callable) -> Binding:
        """
        Creates ``Binding`` from property names on ``self``.

        Args:
            property_names: List of property names of ``self``.
            transform: The function that accepts a new property values and returns the processed value. The values will be passed according to the order in ``property_names``.
        Returns:
            :class:`~ignis.gobject.Binding`
        """
        return Binding(self, property_names, transform)

    def __getattribute__(self, name: str) -> Any:
        # This modified __getattribute__ method redirect all "set_" methods to set_property method to provive bindings support.
        # "get_" method redirect need to widgets that override enums, to make "get_" return strings instead of enums.

        if name.startswith("set_"):
            property_name = name.replace("set_", "")
            if self.find_property(property_name):
                return lambda value: self.set_property(property_name, value)
        elif name.startswith("get_"):
            property_name = name.replace("get_", "")
            if self.find_property(property_name):
                return lambda: self.get_property(property_name)

        return super().__getattribute__(name)


class IgnisProperty(GObject.Property):
    """
    Bases: :obj:`~gi.repository.GObject.Property`.

    Like ``GObject.Property``, but determines the property type automatically based on the return type of the ``getter``.
    You can override this behaviour by explicitly passing ``type`` argument to the constructor.
    Arguments for the constructor are the same as for ``GObject.Property``.
    """

    def __init__(
        self,
        getter: Callable | None = None,
        setter: Callable | None = None,
        type: type | None = None,
        default: Any = None,
        nick: str = "",
        blurb: str = "",
        flags: GObject.ParamFlags = GObject.ParamFlags.READWRITE,
        minimum: Any = None,
        maximum: Any = None,
    ):
        processed_type = (
            self.__process_getter_return_type(getter)
            if type is None and getter
            else type
        )
        processed_default = (
            self.__process_default(processed_type)
            if default is None and processed_type
            else default
        )

        super().__init__(
            getter=getter,
            setter=setter,
            type=processed_type,  # type: ignore
            default=processed_default,
            nick=nick,
            blurb=blurb,
            flags=flags,
            minimum=minimum,
            maximum=maximum,
        )

    def __process_getter_return_type(self, getter: Callable) -> type | None:
        getter_return_type = getter.__annotations__.get("return", None)
        type_: type | None = None
        if getter_return_type:
            if isinstance(getter_return_type, UnionType):
                type_ = self.__get_type_from_union(getter_return_type)
            elif get_origin(getter_return_type) is Literal:
                type_ = self.__get_type_from_literal(getter_return_type)
            else:
                type_ = getter_return_type
        else:
            return object

        try:
            # check is valid type
            # a little bit hacky, but why rewrite ready-made code, right?
            self._type_from_python(type_)  # type: ignore
            return type_
        except TypeError:
            return object

    def __process_default(self, tp: type) -> Any:
        if "sphinx" in sys.modules:
            return None

        if tp is bool:
            return False
        elif tp is float:
            return 0.0
        elif issubclass(tp, GObject.GFlags):
            # gflags has  __flags_values__ attr, trust me
            first_value = list(tp.__flags_values__.values())[0]  # type: ignore
            return first_value

    def __get_type_from_union(self, tp: UnionType) -> type:
        non_none_types = tuple(t for t in tp.__args__ if t is not type(None))
        if len(non_none_types) == 1:
            return non_none_types[0]
        else:
            return object

    def __get_type_from_literal(self, tp: type) -> type | None:
        values = get_args(tp)
        return type(values[0]) if values else None


class IgnisSignal(GObject.Signal):
    """
    Bases: :obj:`~gi.repository.GObject.Signal`.

    The same as ``GObject.Signal``, nothing special.
    This class is needed only for the correct determination of signals when building docs.
    """
