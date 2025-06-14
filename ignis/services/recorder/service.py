import signal
import asyncio
import datetime
import subprocess
from ignis.base_service import BaseService
from ignis.gobject import IgnisProperty, IgnisSignal
from ignis.exceptions import GpuScreenRecorderError
from loguru import logger
from .config import RecorderConfig
from .capture_option import CaptureOption
from .audio_device import AudioDevice


class RecorderService(BaseService):
    """
    A screen recorder. Uses ``gpu-screen-recorder`` as the backend.

    There are options available for this service: :class:`~ignis.options.Options.Recorder`.

    Example usage:

    .. code-block:: python

        import asyncio
        from ignis.services.recorder import RecorderService, RecorderConfig

        recorder = RecorderService.get_default()

        # You can create a configuration from the options
        rec_config = RecorderConfig.new_from_options()

        # You can override them for this config
        rec_config.cursor = False

        # Manual creation of configuration
        rec_config = RecorderConfig(
            source="portal",  # You can also pass a monitor name here
            path="path/to/file",
            # only source and path are required btw
            # arguments below are optional
            video_codec="h264",
            framerate=144,
            cursor=True,
            # "default_input" for microphone
            # "default_output" for internal audio
            # "default_output|default_input" for both
            audio_devices=["default_output"],
            # and a lot more...
        )

        # Start recording
        asyncio.create_task(recorder.start_recording(config=rec_config))

        # Stop recording
        recorder.stop_recording()

        # Pause recording
        recorder.pause_recording()

        # Continue recording
        recorder.continue_recording()

        # You can list available capture options (sources)
        print(recorder.list_capture_options())

        # And audio devices
        print(recorder.list_audio_devices())
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

    async def start_recording(self, config: RecorderConfig) -> None:
        """
        Start recording.
        This function exits when recording ends.

        Args:
            config: The recorder configuration.
        Raises:
            GpuScreenRecorderError: If an error occurs during recording.
        """

        cmd_args: list[str] = []

        cmd_options: dict[str, str] = {}

        for key, value in {
            "-w": config.source,
            "-s": config.resolution_limit,
            "-region": config.region,
            "-o": datetime.datetime.now().strftime(config.path)
            if config.format_time
            else config.path,
            "-f": str(config.framerate) if config.framerate else None,
            "-q": config.quality,
            "-ac": config.audio_codec,
            "-ab": str(config.audio_bitrate) if config.audio_bitrate else None,
            "-bm": config.bitrate_mode,
            "-cr": config.color_range,
            "-k": config.video_codec,
            "-fm": config.framerate_mode,
            "-cursor": config.cursor,
            "-encoder": config.encoder,
        }.items():
            if value is not None:
                cmd_options[key] = value

        if config.audio_devices:
            for device in config.audio_devices:
                cmd_args.extend(["-a", device])

        for key, value in cmd_options.items():
            cmd_args.extend([key, value])

        for key, value in config.extra_args.items():
            cmd_args.extend([key, value])

        logger.debug(f"Running gpu-screen-recorder with args:\n{cmd_args}")

        self._process = await asyncio.create_subprocess_exec(
            "gpu-screen-recorder",
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

    def __set_paused(self, value: bool) -> None:
        if not self._process:
            return

        self._is_paused = value
        self._process.send_signal(signal.SIGUSR2)
        self.notify("is-paused")

    def pause_recording(self) -> None:
        """
        Pause recording. This has an effect only if the recording is active and not already paused.
        """
        if not self._is_paused:
            self.__set_paused(True)

    def continue_recording(self) -> None:
        """
        Continue recording. This has an effect only if the recording is active and paused.
        """
        if self._is_paused:
            self.__set_paused(False)

    def __process_list_stdout(self, stdout: str) -> list[str]:
        if stdout == "":
            return []

        return stdout.strip().split("\n")

    def __get_list(self, cmd: str) -> list[str]:
        proc = subprocess.run(
            ["gpu-screen-recorder", cmd], text=True, capture_output=True
        )
        if proc.returncode != 0:
            raise GpuScreenRecorderError(returncode=proc.returncode, stderr=proc.stderr)

        return self.__process_list_stdout(proc.stdout)

    async def __get_list_async(self, cmd: str) -> list[str]:
        proc = await asyncio.create_subprocess_exec(
            "gpu-screen-recorder",
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        bstdout, bstderr = await proc.communicate()

        if proc.returncode != 0:
            raise GpuScreenRecorderError(
                returncode=proc.returncode, stderr=bstderr.decode()
            )

        return self.__process_list_stdout(bstdout.decode())

    def __parse_capture_options(
        self, capture_options: list[str]
    ) -> list[CaptureOption]:
        result = []
        for i in capture_options:
            if "|" not in i:
                result.append(CaptureOption(option=i))
            else:
                name, resolution = i.split("|", 1)

                result.append(CaptureOption(option=name, monitor_resolution=resolution))

        return result

    def __parse_audio_devices(self, audio_devices: list[str]) -> list[AudioDevice]:
        result = []

        for i in audio_devices:
            name, human_readable_name = i.split("|")
            result.append(
                AudioDevice(device_name=name, human_readable_name=human_readable_name)
            )

        return result

    def list_capture_options(self) -> list[CaptureOption]:
        """
        List available capture options.

        Returns:
            A list of available capture options.
        """
        return self.__parse_capture_options(self.__get_list("--list-capture-options"))

    async def list_capture_options_async(self) -> list[CaptureOption]:
        """
        Asynchronous version of :func:`list_capture_options`.

        Returns:
            A list of available capture options.
        """
        return self.__parse_capture_options(
            await self.__get_list_async("--list-capture-options")
        )

    def list_audio_devices(self) -> list[AudioDevice]:
        """
        List audio devices.

        Returns:
            A list of audio devices.
        """
        return self.__parse_audio_devices(self.__get_list("--list-audio-devices"))

    async def list_audio_devices_async(self) -> list[AudioDevice]:
        """
        Asynchronous version of :func:`list_audio_devices`.

        Returns:
            A list of audio devices.
        """
        return self.__parse_audio_devices(
            await self.__get_list_async("--list-audio-devices")
        )

    def list_application_audio(self) -> list[str]:
        """
        List applications that you can record audio from.

        Returns:
            A list of applications that you can record audio from.
        """
        return self.__get_list("--list-application-audio")

    async def list_application_audio_async(self) -> list[str]:
        """
        Asynchronous version of :func:`list_application_audio`.

        Returns:
            A list of applications that you can record audio from.
        """
        return await self.__get_list_async("--list-application-audio")
