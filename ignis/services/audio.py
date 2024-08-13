import gi
from gi.repository import GObject
from ignis.gobject import IgnisGObject
from typing import List
from ignis.exceptions import GvcNotFoundError


try:
    gi.require_version("Gvc", "1.0")
    from gi.repository import Gvc
except (ImportError, ValueError):
    raise GvcNotFoundError() from None

SPEAKER_ICON_TEMPLATE = "audio-volume-{}-symbolic"
MICROPHONE_ICON_TEMPLATE = "microphone-sensitivity-{}-symbolic"


class Stream(IgnisGObject):
    """
    An audio stream.
    A general class for speakers, microphones, applications, and recorders.

    Signals:
        - **"removed"** (): Emitted when the stream has been removed.

    Properties:
        - **stream** (``Gvc.MixerStream``, read-only): An instance of ``Gvc.MixerStream``. You typically shouldn't use this property.
        - **application_id** (``str``, read-only): Application ID or ``None``. Usually returns ``None`` xD.
        - **icon_name** (``str``, read-only): Current icon name, depending on ``volume`` and ``is_muted`` properties. Works only for speakers and microphones.
        - **id** (``int``, read-only): ID of the stream.
        - **name** (``str``, read-only): Name of the stream.
        - **description** (``str``, read-only): Description of the stream.
        - **is_muted** (``bool``, read-write): Whether the stream is muted.
        - **volume** (``float``, read-write): Volume of the stream.
        - **is_default** (``bool``, read-only): Whether the stream is default. Works only for speakers and microphones.
    """

    __gsignals__ = {
        "removed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, control: Gvc.MixerControl, stream: Gvc.MixerStream):
        super().__init__()
        self._control = control
        self._stream = stream
        self.__connection_ids = []

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
            self.__connection_ids.append(id_)

        id_ = self._stream.connect(
            "notify::volume", lambda *args: self.notify("icon_name")
        )
        self.__connection_ids.append(id_)
        id_ = self._stream.connect(
            "notify::is-muted", lambda *args: self.notify("icon_name")
        )
        self.__connection_ids.append(id_)

        self.notify_all()

    @GObject.Property
    def stream(self) -> Gvc.MixerStream:
        return self._stream

    @GObject.Property
    def application_id(self) -> str:
        return self._stream.get_application_id()

    @GObject.Property
    def icon_name(self) -> str:
        if isinstance(self.stream, Gvc.MixerSink):
            template = SPEAKER_ICON_TEMPLATE
        elif isinstance(self.stream, Gvc.MixerSource):
            template = MICROPHONE_ICON_TEMPLATE
        else:
            return

        if self.is_muted:
            return template.format("muted")
        elif self.volume > 67:
            return template.format("high")
        elif self.volume > 33:
            return template.format("medium")
        else:
            return template.format("low")

    @GObject.Property
    def id(self) -> int:
        return self._stream.get_id()

    @GObject.Property
    def name(self) -> str:
        return self._stream.get_name()

    @GObject.Property
    def description(self) -> str:
        return self._stream.get_description()

    @GObject.Property
    def is_muted(self) -> bool:
        return self._stream.get_is_muted()

    @is_muted.setter
    def is_muted(self, value: bool) -> None:
        self._stream.set_is_muted(value)
        self._stream.change_is_muted(value)

    @GObject.Property
    def volume(self) -> float:
        return round(self._stream.get_volume() / self._control.get_vol_max_norm() * 100)

    @volume.setter
    def volume(self, value: float):
        self._stream.set_volume(value * self._control.get_vol_max_norm() / 100)
        self._stream.push_volume()

    @GObject.Property
    def is_default(self) -> bool:
        if isinstance(self.stream, Gvc.MixerSink):
            default_stream = self._control.get_default_sink()
        elif isinstance(self.stream, Gvc.MixerSource):
            default_stream = self._control.get_default_source()
        else:
            return

        if not default_stream:
            return

        return default_stream.get_id() == self.id


class DefaultSpeaker(Stream):
    """
    :meta private:
    """

    def __init__(self, control: Gvc.MixerControl):
        super().__init__(control, None)

    def _sync(self) -> None:
        stream = self._control.get_default_sink()
        if not stream:
            return
        self._stream = stream
        self._setup()


class DefaultMicrophone(Stream):
    """
    :meta private:
    """

    def __init__(self, control: Gvc.MixerControl):
        super().__init__(control, None)

    def _sync(self) -> None:
        stream = self._control.get_default_source()
        if not stream:
            return
        self._stream = stream
        self._setup()


class AudioService(IgnisGObject):
    """
    An audio service.
    Allow controlling audio devices.

    .. warning::
        This service uses the PulseAudio backend.
        To use it with PipeWire, install ``pipewire-pulse``.

    Signals:
        - **"speaker-added"** (:class:`~ignis.services.audio.Stream`): Emitted when a speaker is added.
        - **"microphone-added"** (:class:`~ignis.services.audio.Stream`): Emitted when a microphone is added.
        - **"app-added"** (:class:`~ignis.services.audio.Stream`): Emitted when an app is added.
        - **"recorder-added"** (:class:`~ignis.services.audio.Stream`): Emitted when a recorder is added.

    Properties:
        - **control** (``Gvc.MixerControl``, read-only): A instance of ``Gvc.MixerControl``. You typically shouldn't use this property.
        - **speaker** (:class:`~ignis.services.audio.Stream`, read-write): The default speaker.
        - **microphone** (:class:`~ignis.services.audio.Stream`, read-write): The default microphone.
        - **streams** (List[:class:`~ignis.services.audio.Stream`], read-only): List of all streams.
        - **speakers** (List[:class:`~ignis.services.audio.Stream`], read-only): List of speakers.
        - **microphones** (List[:class:`~ignis.services.audio.Stream`], read-only): List of microphones.
        - **apps** (List[:class:`~ignis.services.audio.Stream`], read-only): List of applications currently playing sound.
        - **recorders** (List[:class:`~ignis.services.audio.Stream`], read-only): List of audio recorders.

    **Example usage:**

    .. code-block:: python

        from ignis.service import Service

        audio = Service.get("audio")

        audio.connect("speaker-added", lambda x, speaker: print(speaker.description))
    """

    __gsignals__ = {
        "speaker-added": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (Stream,)),
        "microphone-added": (
            GObject.SignalFlags.RUN_FIRST,
            GObject.TYPE_NONE,
            (Stream,),
        ),
        "app-added": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (Stream,)),
        "recorder-added": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (Stream,)),
    }

    def __init__(self):
        super().__init__()

        self._control = Gvc.MixerControl(name="Ignis audio control")

        self._speaker = DefaultSpeaker(control=self._control)
        self._microphone = DefaultMicrophone(control=self._control)

        self._streams = {}

        self._speakers = {}
        self._microphones = {}
        self._apps = {}
        self._recorders = {}

        self._control.connect(
            "default-sink-changed", lambda *args: self.__default_changed("speaker")
        )
        self._control.connect(
            "default-source-changed", lambda *args: self.__default_changed("microphone")
        )
        self._control.connect("stream-added", self.__add_stream)
        self._control.connect("stream-removed", self.__remove_stream)

        self._control.open()

    def __default_changed(self, _type: str) -> None:
        getattr(self, _type)._sync()
        for stream in getattr(self, f"{_type}s"):
            stream.notify("is_default")

    @GObject.Property
    def control(self) -> Gvc.MixerControl:
        return self._control

    @GObject.Property
    def speaker(self) -> Stream:
        return self._speaker

    @speaker.setter
    def speaker(self, value: Stream):
        self._control.set_default_sink(value.stream)

    @GObject.Property
    def microphone(self) -> Stream:
        return self._microphone

    @microphone.setter
    def microphone(self, value: Stream):
        self._control.set_default_source(value.stream)

    @GObject.Property
    def streams(self) -> List[Stream]:
        return self._streams.values()

    @GObject.Property
    def speakers(self) -> List[Stream]:
        return self._speakers.values()

    @GObject.Property
    def microphones(self) -> List[Stream]:
        return self._microphones.values()

    @GObject.Property
    def apps(self) -> List[Stream]:
        return self._apps.values()

    @GObject.Property
    def recorders(self) -> List[Stream]:
        return self._recorders.values()

    def __add_stream(self, control: Gvc.MixerControl, id: int):
        stream = control.lookup_stream_id(id)
        audio_stream = Stream(stream=stream, control=control)
        stream_type = self.__get_stream_type(stream)
        if stream_type:
            getattr(self, f"_{stream_type}s")[id] = audio_stream
            self._streams[id] = audio_stream
            self.emit(f"{stream_type}-added", audio_stream)
            self.notify(f"{stream_type}s")

    def __remove_stream(self, control: Gvc.MixerControl, id: int):
        audio_stream = self._streams.pop(id)
        stream_type = self.__get_stream_type(audio_stream.stream)
        if stream_type:
            getattr(self, f"_{stream_type}s").pop(id)
            audio_stream.emit("removed")
            self.notify(f"{stream_type}s")

    def __get_stream_type(self, stream: Gvc.MixerStream) -> None:
        if isinstance(stream, Gvc.MixerSink):
            return "speaker"
        elif isinstance(stream, Gvc.MixerSource):
            return "microphone"
        elif isinstance(stream, Gvc.MixerSourceOutput):
            return "recorder"
        elif isinstance(stream, Gvc.MixerSinkInput):
            return "app"
