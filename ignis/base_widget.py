from gi.repository import Gtk, GObject
from typing import Any
from ignis.gobject import IgnisGObject


class BaseWidget(Gtk.Widget, IgnisGObject):
    gproperties = __gproperties__ = {}
    _overrided_enums = {}

    def __init__(
        self,
        setup: callable = None,
        vexpand: bool = False,
        hexpand: bool = False,
        visible: bool = True,
        **kwargs,
    ):
        Gtk.Widget.__init__(self)
        IgnisGObject.__init__(self)

        self._class_name = None
        self._style = None
        self._css_provider = None

        self.vexpand = vexpand
        self.hexpand = hexpand
        self.visible = visible

        self.override_enum("halign", Gtk.Align)
        self.override_enum("valign", Gtk.Align)

        for key in kwargs.keys():
            self.set_property(key, kwargs[key])

        if setup:
            setup(self)

    @GObject.property
    def style(self) -> str:
        return self._style

    @style.setter
    def style(self, value: str) -> None:
        if "{" not in value and "}" not in value:
            value = "* {" + value + "}"

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(value.encode())

        self.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        if self._css_provider:
            self.get_style_context().remove_provider(self._css_provider)
        self._css_provider = css_provider
        self._style = value

    def set_property(self, property_name: str, value: Any) -> None:
        """
        :meta private:
        """
        if property_name in self._overrided_enums:
            super().set_property(
                property_name,
                getattr(self._overrided_enums[property_name], value.upper()),
            )
        else:
            super().set_property(property_name, value)

    def get_property(self, property_name: str) -> Any:
        """
        :meta private:
        """
        if property_name in self._overrided_enums:
            return super().get_property(property_name).value_nick
        else:
            return super().get_property(property_name)

    def __setattr__(self, name: str, value: Any) -> None:
        if self.find_property(name):
            self.set_property(name, value)
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name: str) -> Any:
        if self.find_property(name):
            return self.get_property(name)
        else:
            super().__getattribute__(name)

    def override_enum(self, property_name: str, enum: GObject.GEnum) -> None:
        self._overrided_enums[property_name] = enum
