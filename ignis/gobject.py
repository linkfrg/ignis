from gi.repository import GObject, GLib
from typing import Union, Any, List


class Binding(GObject.Object):
    """
    An object that describe binding.

    Properties:
        - **target** (``GObject.Object``, read-only): Target GObject.
        - **target_property** (``GObject.Object``, read-only): Property on target GObject.
        - **transform** (``GObject.Object``, optional, read-only): The function that accepts a new property value and returns the processed value.

    """

    def __init__(
        self, target: GObject.Object, target_property: str, transform: callable = None
    ):
        self._target = target
        self._target_property = target_property
        self._transform = transform
        super().__init__()

    @GObject.Property
    def target(self) -> GObject.Object:
        return self._target

    @GObject.Property
    def target_property(self) -> str:
        return self._target_property

    @GObject.Property
    def transform(self) -> callable:
        return self._transform


class IgnisGObject(GObject.Object):
    """
    Bases: `GObject.Object <https://lazka.github.io/pgi-docs/index.html#GObject-2.0/classes/Object.html>`_.

    A base class for all services and widgets (and some utils).
    Mainly, it is the same GObject.Object, but with some improvements.

    1. It provides support for :class:`~ignis.gobject.Binding`.
    2. It offers easier control over properties (without the need for the ``.props`` attribute).

    """

    def __init__(self):
        super().__init__()

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

    def notify_all(self, without: Union[List[str], str] = None) -> None:
        """
        Notify all properties.

        Args:
            without (Union[List[str], str], optional): Property or list of properties that will not be notified.
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
        if value is None:
            return
        elif isinstance(value, Binding):
            self.bind_property(
                source_property=property_name,
                target=value.target,
                target_property=value.target_property,
                transform=value.transform,
            )
        else:
            super().set_property(property_name, value)

    def bind_property(
        self,
        source_property: str,
        target: GObject.Object,
        target_property: str,
        transform: callable = None,
    ) -> None:
        """
        Bind ``source_property`` on ``self`` with ``target_property`` on ``target``.

        Args:
            source_property (``str``): The property on ``self`` to bind.
            target (``GObject.Object``): the target ``GObject.Object``.
            target_property (``str``): the property on ``target`` to bind.
            transform (``callable``, optional): The function that accepts a new property value and returns the processed value.
        """

        def callback(*args):
            value = target.get_property(target_property.replace("-", "_"))
            if transform:
                value = transform(value)
            self.set_property(source_property, value)

        target.connect(f"notify::{target_property.replace('_', '-')}", callback)
        callback()

    def bind(self, property_name: str, transform: callable = None) -> Binding:
        """
        Creates ``Binding`` from property name on ``self``.

        Args:
            property_name(``str``): Property name of ``self``.
            transform (``callable``): The function that accepts a new property value and returns the processed value.
        Returns:
            :class:`~ignis.gobject.Binding`
        """
        return Binding(self, property_name, transform)

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
