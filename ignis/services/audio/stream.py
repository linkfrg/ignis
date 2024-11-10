from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisGObject
from typing import Literal, Union
from ._imports import Gvc
from .constants import SPEAKER_ICON_TEMPLATE, MICROPHONE_ICON_TEMPLATE


class Stream(IgnisGObject):
    """
    An audio stream.
    A general class for speakers, microphones, applications, and recorders.

    Raises:
        GvcNotFoundError: If Gvc is not found.
    """

    def __init__(self, control: Gvc.MixerControl, stream: Union[Gvc.MixerStream, None]):
        super().__init__()
        self._control = control
        self._stream = stream
        self._connection_ids: list[int] = []

        self._setup()

    def _setup(self) -> None:
        if not self._stream:
            return

        for property_name in [
            "application_id",
            "id",
            "name",
            "description",
            "is-muted",
            "volume",
        ]:
            id_ = self._stream.connect(
                f"notify::{property_name}",
                lambda *args, property_name=property_name: self.notify(property_name),
            )
            self._connection_ids.append(id_)

        id_ = self._stream.connect(
            "notify::volume", lambda *args: self.notify("icon_name")
        )
        self._connection_ids.append(id_)
        id_ = self._stream.connect(
            "notify::is-muted", lambda *args: self.notify("icon_name")
        )
        self._connection_ids.append(id_)

        self.notify_all()

    @GObject.Signal
    def removed(self):
        """
        - Signal

        Emitted when the stream has been removed.
        """

    @GObject.Property
    def stream(self) -> Union[Gvc.MixerStream, None]:
        """
        - read-only

        An instance of ``Gvc.MixerStream``.
        """
        return self._stream

    @GObject.Property
    def application_id(self) -> str | None:
        """
        - read-only

        The application ID or ``None``.
        """
        if not self._stream:
            return None

        return self._stream.get_application_id()

    @GObject.Property
    def icon_name(self) -> str | None:
        """
        - read-only

        The current icon name, depending on ``volume`` and ``is_muted`` properties.
        Works only for speakers and microphones.
        """
        if isinstance(self.stream, Gvc.MixerSink):
            template = SPEAKER_ICON_TEMPLATE
        elif isinstance(self.stream, Gvc.MixerSource):
            template = MICROPHONE_ICON_TEMPLATE
        else:
            return None

        if self.is_muted:
            return template.format("muted")
        elif self.volume > 67:
            return template.format("high")
        elif self.volume > 33:
            return template.format("medium")
        else:
            return template.format("low")

    @GObject.Property
    def id(self) -> int | None:
        """
        - read-only

        The ID of the stream.
        """
        if not self._stream:
            return None

        return self._stream.get_id()

    @GObject.Property
    def name(self) -> str | None:
        """
        - read-only

        The name of the stream.
        """
        if not self._stream:
            return None

        return self._stream.get_name()

    @GObject.Property
    def description(self) -> str | None:
        """
        - read-only

        The description of the stream.
        """
        if not self._stream:
            return None

        return self._stream.get_description()

    @GObject.Property
    def is_muted(self) -> bool | None:
        """
        - read-only

        Whether the stream is muted.
        """
        if not self._stream:
            return None

        return self._stream.get_is_muted()

    @is_muted.setter
    def is_muted(self, value: bool) -> None:
        self._stream.set_is_muted(value)
        self._stream.change_is_muted(value)

    @GObject.Property
    def volume(self) -> float | None:
        """
        - read-only

        The current volume of the stream.
        """
        if not self._stream:
            return None

        return round(self._stream.get_volume() / self._control.get_vol_max_norm() * 100)

    @volume.setter
    def volume(self, value: float):
        if not self._stream:
            return None

        self._stream.set_volume(value * self._control.get_vol_max_norm() / 100)
        self._stream.push_volume()

    @GObject.Property
    def is_default(self) -> bool:
        """
        - read-only

        Whether the stream is default.
        Works only for speakers and microphones.
        """
        if isinstance(self.stream, Gvc.MixerSink):
            default_stream = self._control.get_default_sink()
        elif isinstance(self.stream, Gvc.MixerSource):
            default_stream = self._control.get_default_source()
        else:
            return False

        if not default_stream:
            return False

        return default_stream.get_id() == self.id


class DefaultStream(Stream):
    """
    :meta private:
    """

    def __init__(self, control: Gvc.MixerControl, _type: Literal["sink", "source"]):
        super().__init__(control, None)
        self._type = _type

    def _sync(self) -> None:
        stream = getattr(self._control, f"get_default_{self._type}")()
        if not stream:
            return
        self._stream = stream
        self._setup()
