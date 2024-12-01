from gi.repository import GObject  # type: ignore
from ignis.base_service import BaseService
from ._imports import Gvc
from .stream import Stream, DefaultStream


class AudioService(BaseService):
    """
    An audio service.
    Allows controlling audio devices.

    .. warning::
        This service uses the PulseAudio backend.
        To use it with PipeWire, install ``pipewire-pulse``.

    Example usage:

    .. code-block:: python

        from ignis.services.audio import AudioService

        audio = AudioService.get_default()
        audio.connect("speaker-added", lambda x, speaker: print(speaker.description))
    """

    def __init__(self):
        super().__init__()

        self._control = Gvc.MixerControl(name="Ignis audio control")

        self._speaker = DefaultStream(control=self._control, _type="sink")
        self._microphone = DefaultStream(control=self._control, _type="source")

        self._streams: dict[int, Stream] = {}

        self._speakers: dict[int, Stream] = {}
        self._microphones: dict[int, Stream] = {}
        self._apps: dict[int, Stream] = {}
        self._recorders: dict[int, Stream] = {}

        self._control.connect("default-sink-changed", self.__default_changed, "speaker")
        self._control.connect(
            "default-source-changed", self.__default_changed, "microphone"
        )
        self._control.connect("stream-added", self.__add_stream)
        self._control.connect("stream-removed", self.__remove_stream)

        self._control.open()

    def __default_changed(self, x, y, _type: str) -> None:
        getattr(self, _type)._sync()
        for stream in getattr(self, f"{_type}s"):
            stream.notify("is_default")

    @GObject.Signal(arg_types=(Stream,))
    def speaker_added(self, *args):
        """
        - Signal

        Emitted when a speaker is added.

        Args:
            stream (:class:`~ignis.services.audio.Stream`): The instance of the stream.
        """

    @GObject.Signal(arg_types=(Stream,))
    def microphone_added(self, *args):
        """
        - Signal

        Emitted when a microphone is added.

        Args:
            stream (:class:`~ignis.services.audio.Stream`): The instance of the stream.
        """

    @GObject.Signal(arg_types=(Stream,))
    def app_added(self, *args):
        """
        - Signal

        Emitted when an app is added.

        Args:
            stream (:class:`~ignis.services.audio.Stream`): The instance of the stream.
        """

    @GObject.Signal(arg_types=(Stream,))
    def recorder_added(self, *args):
        """
        - Signal

        Emitted when a recorder is added.

        Args:
            stream (:class:`~ignis.services.audio.Stream`): The instance of the stream.
        """

    @GObject.Property
    def control(self) -> Gvc.MixerControl:
        """
        - read-only

        An instance of ``Gvc.MixerControl``.
        """
        return self._control

    @GObject.Property
    def speaker(self) -> Stream:
        """
        - read-write

        The default speaker.
        """
        return self._speaker

    @speaker.setter
    def speaker(self, value: Stream):
        self._control.set_default_sink(value.stream)

    @GObject.Property
    def microphone(self) -> Stream:
        """
        - read-write

        The default microphone.
        """
        return self._microphone

    @microphone.setter
    def microphone(self, value: Stream):
        self._control.set_default_source(value.stream)

    @GObject.Property
    def streams(self) -> list[Stream]:
        """
        - read-only

        A list of all streams.
        """
        return list(self._streams.values())

    @GObject.Property
    def speakers(self) -> list[Stream]:
        """
        - read-only

        A list of speakers.
        """
        return list(self._speakers.values())

    @GObject.Property
    def microphones(self) -> list[Stream]:
        """
        - read-only

        A list of microphones.
        """
        return list(self._microphones.values())

    @GObject.Property
    def apps(self) -> list[Stream]:
        """
        - read-only

        A list of applications currently playing sound.
        """
        return list(self._apps.values())

    @GObject.Property
    def recorders(self) -> list[Stream]:
        """
        - read-only

        A list of audio recorders.
        """
        return list(self._recorders.values())

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

    def __get_stream_type(self, stream: Gvc.MixerStream) -> str | None:
        if isinstance(stream, Gvc.MixerSink):
            return "speaker"
        elif isinstance(stream, Gvc.MixerSource):
            return "microphone"
        elif isinstance(stream, Gvc.MixerSourceOutput):
            return "recorder"
        elif isinstance(stream, Gvc.MixerSinkInput):
            return "app"
        else:
            return None
