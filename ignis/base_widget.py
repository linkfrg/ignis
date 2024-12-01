from gi.repository import Gtk, GObject, GLib  # type: ignore
from typing import Any, Callable, Union
from ignis.gobject import IgnisGObject
from ignis.exceptions import CssParsingError


def raise_css_parsing_error(
    css_provider: Gtk.CssProvider, section: Gtk.CssSection, gerror: GLib.GError
) -> None:
    raise CssParsingError(section, gerror)


class BaseWidget(Gtk.Widget, IgnisGObject):
    """
    Bases: :class:`~ignis.gobject.IgnisGObject`.

    The base class for all widgets.
    Provides ``style`` property and allows overriding enums.
    """

    gproperties = __gproperties__ = {}  # type: ignore
    _overrided_enums: dict[str, GObject.GEnum] = {}

    def __init__(
        self,
        setup: Callable | None = None,
        vexpand: bool = False,
        hexpand: bool = False,
        visible: bool = True,
        **kwargs,
    ):
        Gtk.Widget.__init__(self)

        self._style: str | None = None
        self._css_provider: Union[Gtk.CssProvider, None] = None

        self.vexpand = vexpand
        self.hexpand = hexpand
        self.visible = visible

        self.override_enum("halign", Gtk.Align)
        self.override_enum("valign", Gtk.Align)

        IgnisGObject.__init__(self, **kwargs)

        if setup:
            setup(self)

    @GObject.property
    def style(self) -> str | None:
        return self._style

    @style.setter
    def style(self, value: str) -> None:
        if self._css_provider:
            self.get_style_context().remove_provider(self._css_provider)

        if "{" not in value and "}" not in value:
            value = "* {" + value + "}"

        css_provider = Gtk.CssProvider()
        css_provider.connect("parsing-error", raise_css_parsing_error)

        css_provider.load_from_data(value.encode())

        self.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

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

    def override_enum(self, property_name: str, enum: Any) -> None:
        """
        Override an enum.

        Args:
            property_name: The name of the property to override.
            enum(``GObject.GEnum``): An enum that accepts the property to be overridden. For example, for ``valign`` it will be ``Gtk.Align``.
        """
        self._overrided_enums[property_name] = enum
