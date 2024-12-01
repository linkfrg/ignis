import os
import time
import shutil
import requests
import urllib.parse
from ignis.dbus import DBusProxy
from gi.repository import GObject, GLib  # type: ignore
from ignis.gobject import IgnisGObject
from ignis.utils import Utils
from loguru import logger
from .constants import ART_URL_CACHE_DIR


class MprisPlayer(IgnisGObject):
    """
    A media player object.
    """

    def __init__(self, name: str):
        super().__init__()
        self._position: int = -1
        self._art_url: str | None = None

        self.__mpris_proxy = DBusProxy(
            name=name,
            object_path="/org/mpris/MediaPlayer2",
            interface_name="org.mpris.MediaPlayer2",
            info=Utils.load_interface_xml("org.mpris.MediaPlayer2"),
        )

        self.__player_proxy = DBusProxy(
            name=self.__mpris_proxy.name,
            object_path=self.__mpris_proxy.object_path,
            interface_name="org.mpris.MediaPlayer2.Player",
            info=Utils.load_interface_xml("org.mpris.MediaPlayer2.Player"),
        )

        self.__player_proxy.proxy.connect("g-properties-changed", self.__sync)

        self.__mpris_proxy.watch_name(
            on_name_vanished=lambda *args: self.emit("closed")
        )

        os.makedirs(ART_URL_CACHE_DIR, exist_ok=True)

        self.__ready()

    @Utils.run_in_thread
    def __ready(self) -> None:
        self.__sync_position()
        self.__cache_art_url()
        self.emit("ready")

    def __sync(self, proxy, properties: GLib.Variant, invalidated_properties) -> None:
        prop_dict = properties.unpack()

        if "Metadata" in prop_dict.keys():
            self.__cache_art_url()

        self.notify_all(without="art-url")

    @Utils.run_in_thread
    def __cache_art_url(self) -> None:
        art_url = self.metadata.get("mpris:artUrl", None)
        result = None

        if art_url == self._art_url:
            return

        if art_url:
            if art_url.startswith("file://"):
                result = self.__copy_art_url(art_url)

            elif art_url.startswith("https://") or art_url.startswith("http://"):
                result = self.__download_art_url(art_url)

        self._art_url = result
        self.notify("art_url")

    def __copy_art_url(self, art_url: str) -> str:
        path = art_url.replace("file://", "")
        result = ART_URL_CACHE_DIR + "/" + os.path.basename(path)
        if os.path.exists(result):
            return result

        shutil.copy(path, result)

        return result

    def __download_art_url(self, art_url: str) -> str | None:
        result = ART_URL_CACHE_DIR + "/" + self.__get_valid_url_filename(art_url)
        if os.path.exists(result):
            return result

        try:
            status_code = Utils.download_image(art_url, result, timeout=1)
            if status_code != 200:
                logger.warning(
                    f"Failed to download the art image of media. (Status code: {status_code})"
                )
                return None
        except requests.exceptions.ConnectionError:
            logger.warning(
                "Failed to download the art image of media. (Connection Error)"
            )
            return None
        except requests.exceptions.Timeout:
            logger.warning("Failed to download the art image of media. (Timeout)")
            return None

        return result

    def __get_valid_url_filename(self, url: str) -> str:
        parsed_url = urllib.parse.urlparse(url)

        domain = parsed_url.netloc.replace(".", "_")
        path = parsed_url.path.replace("/", "_")
        query = parsed_url.query.replace("&", "_").replace("=", "-")

        filename = f"{domain}{path}_{query}"

        return filename

    @Utils.run_in_thread
    def __sync_position(self) -> None:
        while True:
            position = self.__player_proxy.Position
            if position:
                self._position = position // 1_000_000
                self.notify("position")
            time.sleep(1)

    @GObject.Signal
    def ready(self): ...  # user shouldn't connect to this signal

    @GObject.Signal
    def closed(self):
        """
        - Signal

        Emitted when a player has been closed or removed.
        """

    @GObject.Property
    def can_control(self) -> bool:
        """
        - read-only

        Whether the player can be controlled.
        """
        return self.__player_proxy.CanControl

    @GObject.Property
    def can_go_next(self) -> bool:
        """
        - read-only

        Whether the player can go to the next track.
        """
        return self.__player_proxy.CanGoNext

    @GObject.Property
    def can_go_previous(self) -> bool:
        """
        - read-only

        Whether the player can go to the previous track.
        """
        return self.__player_proxy.CanGoPrevious

    @GObject.Property
    def can_pause(self) -> bool:
        """
        - read-only

        Whether the player can pause.
        """
        return self.__player_proxy.CanPause

    @GObject.Property
    def can_play(self) -> bool:
        """
        - read-only

        Whether the player can play.
        """
        return self.__player_proxy.CanPlay

    @GObject.Property
    def can_seek(self) -> bool:
        """
        - read-only

        Whether the player can seek (change position on track in seconds).
        """
        return self.__player_proxy.CanSeek

    @GObject.Property
    def loop_status(self) -> str:
        """
        - read-only

        The current loop status.
        """
        return self.__player_proxy.LoopStatus

    @GObject.Property
    def metadata(self) -> dict:
        """
        - read-only

        A dictionary containing metadata.
        """
        metadata = getattr(self.__player_proxy, "Metadata", None)
        if metadata:
            return metadata
        else:
            return {}

    @GObject.Property
    def track_id(self) -> str:
        """
        - read-only

        The ID of the current track.
        """
        return self.metadata.get("mpris:trackid", None)

    @GObject.Property
    def length(self) -> int:
        """
        - read-only

        The length of the current track,
        ``-1`` if not supported by the player.
        """
        length = self.metadata.get("mpris:length", None)
        if length:
            return length // 1_000_000
        else:
            return -1

    @GObject.Property
    def art_url(self) -> str | None:
        """
        - read-only

        The path to the cached art image of the track.
        """
        return self._art_url

    @GObject.Property
    def album(self) -> str | None:
        """
        - read-only

        The current album name.
        """
        return self.metadata.get("xesam:album", None)

    @GObject.Property
    def artist(self) -> str | None:
        """
        - read-only

        The current artist name.
        """
        artist = self.metadata.get("xesam:artist", None)
        if isinstance(artist, list):
            return "".join(artist)
        else:
            return artist

    @GObject.Property
    def title(self) -> str | None:
        """
        - read-only

        The current title of the track.
        """
        return self.metadata.get("xesam:title", None)

    @GObject.Property
    def url(self) -> str | None:
        """
        - read-only

        The URL address of the track.
        """
        return self.metadata.get("xesam:url", None)

    @GObject.Property
    def playback_status(self) -> str:
        """
        - read-only

        The current playback status. Can be "Playing" or "Paused".
        """
        return self.__player_proxy.PlaybackStatus

    @GObject.Property
    def position(self) -> int:
        """
        - read-write

        The current position in the track in seconds.
        """
        return self._position

    @position.setter
    def position(self, value: int) -> None:
        self.__player_proxy.SetPosition(
            "(ox)", self.track_id, value * 1_000_000, result_handler=lambda *args: None
        )

    @GObject.Property
    def shuffle(self) -> bool:
        """
        - read-only

        The shuffle status.
        """
        return self.__player_proxy.Shuffle

    @GObject.Property
    def volume(self) -> float:
        """
        - read-only

        The volume of the player.
        """
        return self.__player_proxy.Volume

    @GObject.Property
    def identity(self) -> str:
        """
        - read-only

        The name of the player (e.g. "Spotify", "firefox").
        """
        return self.__mpris_proxy.Identity

    @GObject.Property
    def desktop_entry(self) -> str:
        """
        - read-only

        The .desktop file of the player.
        """
        return self.__mpris_proxy.DesktopEntry

    def next(self) -> None:
        """
        Go to the next track.
        """
        self.__player_proxy.Next(result_handler=lambda *args: None)

    def previous(self) -> None:
        """
        Go to the previous track.
        """
        self.__player_proxy.Previous(result_handler=lambda *args: None)

    def pause(self) -> None:
        """
        Pause playback.
        """
        self.__player_proxy.Pause(result_handler=lambda *args: None)

    def play(self) -> None:
        """
        Start playback.
        """
        self.__player_proxy.Play(result_handler=lambda *args: None)

    def play_pause(self) -> None:
        """
        Toggle between playing and pausing.
        """
        self.__player_proxy.PlayPause(result_handler=lambda *args: None)

    def stop(self) -> None:
        """
        Stop playback and remove the MPRIS interface if supported by the player.
        """
        self.__player_proxy.Stop(result_handler=lambda *args: None)

    def seek(self, offset: int) -> None:
        """
        Seek to a specific position in the track.
        Positive values move forward, and negative values move backward.
        The offset is in milliseconds.
        """
        self.__player_proxy.Seek(
            "(x)", offset * 1_000_100, result_handler=lambda *args: None
        )
