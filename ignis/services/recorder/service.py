import os
import signal
import asyncio
import datetime
import subprocess
from ignis.app import IgnisApp
from ignis.base_service import BaseService
from ignis.options import options
from ignis.gobject import IgnisProperty, IgnisSignal
from ignis.exceptions import GpuScreenRecorderError
from typing import Literal
from loguru import logger

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

        self._active: bool = False
        self._is_paused: bool = False

        self._process: asyncio.subprocess.Process | None = None

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

    async def start_recording(
        self,
        source: Literal["screen", "screen-direct", "focused", "portal", "region"] | str,
        path: str | None = None,
        resolution_limit: str | None = None,
        region: str | None = None,
        framerate: int | None = None,
        audio_devices: list[str] | None = None,
        quality: Literal["medium", "high", "very_high", "ultra"] | None = None,
        video_codec: Literal[
            "auto",
            "h264",
            "hevc",
            "av1",
            "vp8",
            "vp9",
            "hevc_hdr",
            "av1_hdr",
            "hevc_10bit",
            "av1_10bit",
        ]
        | None = None,
        audio_codec: Literal["aac", "opus", "flac"] | None = None,
        audio_bitrate: int | None = None,
        framerate_mode: Literal["cfr", "vfr", "content"] | None = None,
        bitrate_mode: Literal["auto", "qp", "vbr", "cbr"] | None = None,
        color_range: Literal["limited", "full"] | None = None,
        cursor: Literal["yes", "no"] | None = None,
        encoder: Literal["gpu", "cpu"] | None = None,
        *extra_args,
    ) -> None:
        """
        Start recording.
        """

        cmd_args: list[str] = ["gpu-screen-recorder"]

        cmd_options: dict[str, str] = {}

        for key, value in {
            "-w": source,
            "-s": resolution_limit,
            "-region": region,
            "-o": path,
            "-f": str(framerate) if framerate else None,
            "-q": quality,
            "-ac": audio_codec,
            "-ab": str(audio_bitrate) if audio_bitrate else None,
            "-bm": bitrate_mode,
            "-cr": color_range,
            "-k": video_codec,
            "-fm": framerate_mode,
            "-cursor": cursor,
            "-encoder": encoder,
        }.items():
            if value is not None:
                cmd_options[key] = value

        if not path:
            cmd_options["-o"] = os.path.join(
                options.recorder.default_file_location,  # type: ignore
                datetime.datetime.now().strftime(options.recorder.default_filename),
            )

        if audio_devices:
            for device in audio_devices:
                cmd_args.extend(["-a", device])

        for key, value in cmd_options.items():
            cmd_args.extend([key, value])

        cmd_args.extend(extra_args)

        logger.debug(f"Running gpu-screen-recorder with args:\n{cmd_args}")

        self._process = await asyncio.create_subprocess_exec(
            *cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self._active = True
        self._is_paused = False

        self.notify("active")
        self.notify("is-paused")
        self.emit("recording-started")

        bstdout, bstderr = await self._process.communicate()

        stdout = bstdout.decode().strip()
        stderr = bstderr.decode().strip()

        logger.debug(
            f"gpu-screen-recorder exited with returncode: {self._process.returncode}\nstdout:\n{stdout}\nstderr:\n{stderr}"
        )

        if self._process.returncode != 0:
            self.__recording_error(self._process.returncode, stderr)

    def __recording_error(self, returncode: int | None, stderr: str) -> None:
        self._active = False
        self._is_paused = False
        self.notify("active")
        self.notify("is-paused")

        raise GpuScreenRecorderError(returncode=returncode, stderr=stderr)

    def stop_recording(self) -> None:
        """
        Stop recording.
        """
        if not self._process:
            return

        self._process.send_signal(signal.SIGINT)

        self._active = False
        self._is_paused = False

        self.notify("active")
        self.notify("is-paused")
        self.emit("recording_stopped")

    def pause_recording(self) -> None:
        """
        Pause recording. This has an effect only if the recording is active and not already paused.
        """
        if not self._process:
            return

        self._is_paused = True
        self._process.send_signal(signal.SIGUSR2)
        self.notify("is-paused")

    def continue_recording(self) -> None:
        """
        Continue recording. This has an effect only if the recording is active and paused.
        """
        if not self._process:
            return

        self._is_paused = False
        self._process.send_signal(signal.SIGUSR2)
        self.notify("is-paused")
