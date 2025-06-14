import datetime
from gi.repository import GLib  # type: ignore
from ignis.app import IgnisApp
from ignis.services.audio import AudioService
from ignis.exceptions import GstPluginNotFoundError
from ignis.base_service import BaseService
from ignis.options import options
from ignis.gobject import IgnisProperty, IgnisSignal
from .session import SessionManager
from .util import gst_inspect
from ._imports import Gst
from .constants import PIPELINE_TEMPLATE, MAIN_AUDIO_PIPELINE, AUDIO_DEVICE_PIPELINE

app = IgnisApp.get_default()


class RecorderService(BaseService):
    """
    A screen recorder.
    Uses XDG Desktop portal and PipeWire.
    Allow record screen with microphone audio and internal system audio.

    There are options available for this service: :class:`~ignis.options.Options.Recorder`.

    Dependencies:
        - GStreamer
        - PipeWire
        - gst-plugin-pipewire
        - gst-plugins-good
        - gst-plugins-ugly
        - pipewire-pulse: for audio recording.

    Raises:
        GstNotFoundError: If GStreamer is not found.
        GstPluginNotFoundError: If GStreamer plugin is not found.

    Example usage:

    .. code-block:: python

        from ignis.services.recorder import RecorderService
        from ignis import utils

        recorder = RecorderService.get_default()

        recorder.start_recording(record_internal_audio=True)

        # record for 30 seconds and then stop
        utils.Timeout(ms=30 * 1000, target=recorder.stop_recording)
    """

    def __init__(self):
        super().__init__()
        self.__check_deps()
        Gst.init(None)

        self.__manager = SessionManager()

        self._active: bool = False
        self._is_paused: bool = False
        self.__pipeline: Gst.Element | None = None

        self._N_THREADS: str = str(min(max(1, GLib.get_num_processors()), 64))

        self._audio = AudioService.get_default()

        app.connect("shutdown", lambda x: self.stop_recording())

    def __check_deps(self) -> None:
        if not gst_inspect("pipewiresrc"):
            raise GstPluginNotFoundError("PipeWire", "gst-plugin-pipewire")

        if not gst_inspect("x264enc"):
            raise GstPluginNotFoundError("H.264 encoder", "gst-plugins-ugly")

        if not gst_inspect("mp4mux"):
            raise GstPluginNotFoundError("MP4 muxer", "gst-plugins-good")

    @IgnisSignal
    def recording_started(self):
        """
        Emitted when recording starts.
        """

    @IgnisSignal
    def recording_stopped(self):
        """
        Emitted when recording stops.
        """

    @IgnisProperty
    def active(self) -> bool:
        """
        Whether recording is currently active.
        """
        return self._active

    @IgnisProperty
    def is_paused(self) -> bool:
        """
        Whether recording is currently paused.
        """
        return self._is_paused

    def start_recording(
        self,
        path: str | None = None,
        record_microphone: bool = False,
        record_internal_audio: bool = False,
        audio_devices: list[str] | None = None,
    ) -> None:
        """
        Start recording.

        Args:
            path: Recording path. It will override ``default_file_location`` and ``default_filename`` properties.
            record_microphone: Whether record audio from microphone.
            record_internal_audio: Whether record internal audio.
            audio_devices: A list of audio devices names from which audio should be recorded.
        """

        if path is None:
            path = f"{options.recorder.default_file_location}/{datetime.datetime.now().strftime(options.recorder.default_filename)}"

        pipeline_description = (
            PIPELINE_TEMPLATE.replace("{n_threads}", self._N_THREADS)
            .replace("{path}", path)
            .replace("{bitrate}", str(options.recorder.bitrate))
        )

        audio_pipeline = ""

        if record_microphone:
            audio_pipeline = self.__combine_audio_pipeline(
                audio_pipeline, self._audio.microphone.name
            )

        if record_internal_audio:
            audio_pipeline = self.__combine_audio_pipeline(
                audio_pipeline, self._audio.speaker.name + ".monitor"
            )

        if audio_devices:
            for device in audio_devices:
                audio_pipeline = self.__combine_audio_pipeline(audio_pipeline, device)

        pipeline_description += audio_pipeline

        self.__manager.start_session(self.__play_pipewire_stream, pipeline_description)

    def __combine_audio_pipeline(self, audio_pipeline: str, device: str) -> str:
        if audio_pipeline != "":
            template = AUDIO_DEVICE_PIPELINE
        else:
            template = MAIN_AUDIO_PIPELINE

        audio_pipeline += template.replace("{device}", device)
        return audio_pipeline

    def stop_recording(self) -> None:
        """
        Stop recording.
        """
        if not self.__pipeline:
            return

        self.__pipeline.send_event(Gst.Event.new_eos())

        bus = self.__pipeline.get_bus()
        if not bus:
            return

        bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS)

        self.__pipeline.set_state(Gst.State.NULL)

        self.__pipeline = None
        self._pipeline_description = ""
        self._active = False
        self._is_paused = False
        self.notify("active")
        self.notify("is-paused")
        self.emit("recording_stopped")

    def pause_recording(self) -> None:
        """
        Pause recording. This has an effect only if the recording is active and not already paused.
        """
        if self.__pipeline:
            self._is_paused = True
            self.__pipeline.set_state(Gst.State.PAUSED)
            self.notify("is-paused")

    def continue_recording(self) -> None:
        """
        Continue recording. This has an effect only if the recording is active and paused.
        """
        if self.__pipeline:
            self._is_paused = False
            self.__pipeline.set_state(Gst.State.PLAYING)
            self.notify("is-paused")

    def __play_pipewire_stream(self, node_id: int, pipeline_description: str) -> None:
        pipeline_description = pipeline_description.replace("{node_id}", str(node_id))

        self.__pipeline = Gst.parse_launch(pipeline_description)
        self.__pipeline.set_state(Gst.State.PLAYING)
        bus = self.__pipeline.get_bus()
        if not bus:
            return

        bus.connect("message", self.__on_gst_message)

        self._active = True
        self._is_paused = False

        self.notify("active")
        self.notify("is-paused")
        self.emit("recording_started")

    def __on_gst_message(self, bus, message):
        if message.type == Gst.MessageType.EOS or message.type == Gst.MessageType.ERROR:
            self.stop_recording()
