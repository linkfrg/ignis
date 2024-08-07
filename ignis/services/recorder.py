import gi
import subprocess
import datetime
from gi.repository import GObject, GLib
from ignis.gobject import IgnisGObject
from ignis.dbus import DBusProxy
from ignis.app import app
from ignis.services import Service
from ignis.utils import Utils
from typing import List

options = Service.get("options")
audio = Service.get("audio")

RECORDING_BITRATE_OPTION = "recording_bitrate"
RECORDING_DEFAULT_FILE_LOCATION_OPTION = "recording_default_file_location"
RECORDING_DEFAULT_FILENAME_OPTION = "recording_default_filename"

options.create_option(name=RECORDING_BITRATE_OPTION, default=8000, exists_ok=True)
options.create_option(
    name=RECORDING_DEFAULT_FILE_LOCATION_OPTION,
    default=GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_VIDEOS),
    exists_ok=True,
)
options.create_option(
    name=RECORDING_DEFAULT_FILENAME_OPTION,
    default="%Y-%m-%d_%H-%M-%S.mp4",
    exists_ok=True,
)

N_THREADS = str(min(max(1, GLib.get_num_processors()), 64))


class GstNotFoundError(Exception):
    """
    Raised when GStreamer is not found.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "GStreamer not found! To use the recorder service, install GStreamer", *args
        )


class GstPluginNotFoundError(Exception):
    """
    Raised when a GStreamer plugin is not found.
    """

    def __init__(self, name: str, plugin_package: str, *args) -> None:
        super().__init__(
            f"{name} GStreamer plugin not found! To use the recorder service, install {plugin_package}",
            *args,
        )


def gst_inspect(name: str) -> None:
    try:
        subprocess.run(["gst-inspect-1.0", "--exists", name], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


try:
    gi.require_version("Gst", "1.0")
    from gi.repository import Gst
except (ImportError, ValueError):
    raise GstNotFoundError(
        "GStreamer not found! To use the recorder service, install GStreamer."
    ) from None

PIPELINE_TEMPLATE = """
    pipewiresrc path={node_id} do-timestamp=true keepalive-time=1000 resend-last=true !
    videoconvert chroma-mode=none dither=none matrix-mode=output-only n-threads={n_threads} !
    queue !
    x264enc bitrate={bitrate} threads={n_threads} !
    queue !
    h264parse !
    mp4mux fragment-duration=500 fragment-mode=first-moov-then-finalise name=mux !
    filesink location={path}
    """

MAIN_AUDIO_PIPELINE = """
    pulsesrc device={device} !
    queue !
    audioconvert !
    audioresample !
    audiomixer name=mix !
    queue !
    opusenc !
    mux.
"""

AUDIO_DEVICE_PIPELINE = """
    pulsesrc device={device} !
    queue !
    audioconvert !
    audioresample !
    mix.
"""


class RecorderService(IgnisGObject):
    """
    A screen recorder.
    Uses XDG Desktop portal and PipeWire.
    Allow record screen with microphone audio and internal system audio.

    **Dependencies**:
        - **GStreamer**
        - **PipeWire**
        - **gst-plugin-pipewire**
        - **gst-plugins-good**
        - **gst-plugins-ugly**
        - **pipewire-pulse**: for audio recording.

    Signals:
        - **"recording_started"** (): Emitted when recording starts.
        - **"recording_stopped"** (): Emitted when recording stops.

    Properties:
        - **active** (``bool``, read-write): Whether recording is currently active.
        - **bitrate** (``int``, read-write, default: 8000): The bitrate of the recording.
        - **default_file_location** (``str``, read-write, default: ``"$HOME/Videos"``): Default location for saving recordings.
        - **default_filename** (``str``, read-write, default: ``"%Y-%m-%d_%H-%M-%S.mp4"``): Default filename for recordings. Supports time formating.

    **Example usage:**

    .. code-block:: python

        from ignis.services import Service
        from ignis.utils import Utils

        recorder = Service.get("recorder")

        recorder.start_recording(record_internal_audio=True)

        # record for 30 seconds and then stop
        Utils.Timeout(ms=30 * 1000, target=recorder.stop_recording)
    """

    __gsignals__ = {
        "recording_started": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "recording_stopped": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        super().__init__()
        self.__check_deps()
        Gst.init(None)
        self.__dbus = DBusProxy(
            name="org.freedesktop.portal.Desktop",
            object_path="/org/freedesktop/portal/desktop",
            interface_name="org.freedesktop.portal.ScreenCast",
            info=Utils.load_interface_xml("org.freedesktop.portal.ScreenCast"),
        )
        self._session_token_counter = 0
        self._request_token_counter = 0
        self._active = False
        self._pipeline_description = ""
        self.__pipeline = None

        self._sender_name = (
            self.__dbus.connection.get_unique_name().replace(".", "_").replace(":", "")
        )
        app.connect("quit", lambda x: self.stop_recording())

    def __check_deps(self) -> None:
        if not gst_inspect("pipewiresrc"):
            raise GstPluginNotFoundError("PipeWire", "gst-plugin-pipewire")

        if not gst_inspect("x264enc"):
            raise GstPluginNotFoundError("H.264 encoder", "gst-plugins-ugly")

        if not gst_inspect("mp4mux"):
            raise GstPluginNotFoundError("MP4 muxer", "gst-plugins-good")

    @GObject.Property
    def active(self) -> bool:
        return self._active

    @GObject.Property
    def bitrate(self) -> int:
        return options.get_option(RECORDING_BITRATE_OPTION)

    @bitrate.setter
    def bitrate(self, value: int) -> None:
        options.set_option(RECORDING_BITRATE_OPTION, value)

    @GObject.Property
    def default_file_location(self) -> str:
        return options.get_option(RECORDING_DEFAULT_FILE_LOCATION_OPTION)

    @default_file_location.setter
    def default_file_location(self, value: str) -> None:
        options.set_option(RECORDING_DEFAULT_FILE_LOCATION_OPTION, value)

    @GObject.Property
    def default_filename(self) -> str:
        return options.get_option(RECORDING_DEFAULT_FILENAME_OPTION)

    @default_filename.setter
    def default_filename(self, value: str) -> None:
        options.set_option(RECORDING_DEFAULT_FILENAME_OPTION, value)

    def start_recording(
        self,
        path: str = None,
        record_microphone: bool = False,
        record_internal_audio: bool = False,
        audio_devices: List[str] = None,
    ) -> None:
        """
        Start recording.

        Args:
            path (``str``, optional): Recording path. It will override ``default_file_location`` and ``default_filename`` properties.
            record_microphone (``bool``, optional): Whether record audio from microphone.
            record_internal_audio (``bool``, optional): Whether record internal audio.
            audio_devices (``List[str]``, optional): List of audio devices names from which audio should be recorded.
        """

        if path is None:
            path = f"{self.default_file_location}/{datetime.datetime.now().strftime(self.default_filename)}"

        self._pipeline_description = (
            PIPELINE_TEMPLATE.replace("{n_threads}", N_THREADS)
            .replace("{path}", path)
            .replace("{bitrate}", str(self.bitrate))
        )

        audio_pipeline = ""

        if record_microphone:
            audio_pipeline = self.__combine_audio_pipeline(
                audio_pipeline, audio.microphone.name
            )

        if record_internal_audio:
            audio_pipeline = self.__combine_audio_pipeline(
                audio_pipeline, audio.speaker.name + ".monitor"
            )

        if audio_devices:
            for device in audio_devices:
                audio_pipeline = self.__combine_audio_pipeline(audio_pipeline, device)

        self._pipeline_description += audio_pipeline

        self.__create_session()

    def __combine_audio_pipeline(self, audio_pipeline: str, device: str) -> None:
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
        if self.__pipeline:
            self.__pipeline.send_event(Gst.Event.new_eos())
            self.__pipeline = None
            self._pipeline_description = ""
            self._active = False
            self.notify("active")
            self.emit("recording_stopped")

    def __create_session(self) -> None:
        request_token = self.__request_response(self.__on_create_session_response)
        self._session_token_counter += 1
        session_token = f"u{self._session_token_counter}"
        self.__dbus.CreateSession(
            "(a{sv})",
            {
                "session_handle_token": GLib.Variant("s", session_token),
                "handle_token": GLib.Variant("s", request_token),
            },
        )

    def __request_response(self, callback: callable) -> str:
        self._request_token_counter += 1
        request_token = f"u{self._request_token_counter}"
        request_path = f"/org/freedesktop/portal/desktop/request/{self._sender_name}/{request_token}"
        request_proxy = DBusProxy(
            name="org.freedesktop.portal.Desktop",
            object_path=request_path,
            interface_name="org.freedesktop.portal.Request",
            info=Utils.load_interface_xml("org.freedesktop.portal.Request"),
        )

        request_proxy.signal_subscribe(
            signal_name="Response",
            callback=callback,
        )

        return request_token

    def __on_create_session_response(self, *args):
        response = args[5]
        response_code = response[0]
        self._session = response[1]["session_handle"]

        if response_code != 0:
            self.stop_recording()
            return

        request_token = self.__request_response(self.__on_select_sources_response)

        self.__dbus.SelectSources(
            "(oa{sv})",
            self._session,
            {
                "handle_token": GLib.Variant("s", request_token),
                "multiple": GLib.Variant("b", False),
                "types": GLib.Variant("u", 1 | 2),
            },
        )

    def __on_select_sources_response(self, *args) -> None:
        response_code = args[5][0]

        if response_code != 0:
            self.stop_recording()
            return

        request_token = self.__request_response(self.__on_start_response)
        self.__dbus.Start(
            "(osa{sv})",
            self._session,
            "",
            {
                "handle_token": GLib.Variant("s", request_token),
            },
        )

    def __on_start_response(self, *args):
        results = args[5][1]
        response_code = args[5][0]
        if response_code != 0:
            self.stop_recording()
            return

        for node_id, _stream_properties in results["streams"]:
            self.__play_pipewire_stream(node_id)

    def __play_pipewire_stream(self, node_id: int) -> None:
        self._pipeline_description = self._pipeline_description.replace(
            "{node_id}", str(node_id)
        )
        self.__pipeline = Gst.parse_launch(self._pipeline_description)
        self.__pipeline.set_state(Gst.State.PLAYING)
        self.__pipeline.get_bus().connect("message", self.__on_gst_message)
        self._active = True
        self.notify("active")
        self.emit("recording_started")

    def __on_gst_message(self, bus, message):
        if message.type == Gst.MessageType.EOS or message.type == Gst.MessageType.ERROR:
            self.stop_recording()
