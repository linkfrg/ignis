import os
from collections.abc import Callable
import urllib.parse
from ignis.dbus import DBusProxy
from gi.repository import GObject, GLib  # type: ignore
from ignis.gobject import IgnisGObject
from ignis.utils import Utils
from .constants import ART_URL_CACHE_DIR


class MprisPlayer(IgnisGObject):
    """
    A media player object.
    """

    def __init__(self, name: str):
        super().__init__()

        self._can_control: bool = False
        self._can_go_next: bool = False
        self._can_go_previous: bool = False
        self._can_pause: bool = False
        self._can_play: bool = False
        self._can_seek: bool = False
        self._loop_status: str | None = None
        self._metadata: dict = {}
        self._playback_status: str | None = None
        self._position: int = -1
        self._shuffle: bool = False
        self._volume: int = -1
        self._identity: str | None = None
        self._desktop_entry: str | None = None

        # depend on metadata
        self._track_id: str | None = None
        self._length: int = -1
        self._art_url: str | None = None
        self._album: str | None = None
        self._artist: str | None = None
        self._title: str | None = None
        self._url: str | None = None

        os.makedirs(ART_URL_CACHE_DIR, exist_ok=True)

        DBusProxy.new_async(
            name=name,
            object_path="/org/mpris/MediaPlayer2",
            interface_name="org.mpris.MediaPlayer2",
            info=Utils.load_interface_xml("org.mpris.MediaPlayer2"),
            callback=self.__on_mpris_proxy_initialized,
        )

    def __on_mpris_proxy_initialized(self, proxy: DBusProxy) -> None:
        self.__mpris_proxy = proxy
        self.__mpris_proxy.watch_name(on_name_vanished=lambda *_: self.emit("closed"))

        DBusProxy.new_async(
            name=self.__mpris_proxy.name,
            object_path=self.__mpris_proxy.object_path,
            interface_name="org.mpris.MediaPlayer2.Player",
            info=Utils.load_interface_xml("org.mpris.MediaPlayer2.Player"),
            callback=self.__on_player_proxy_initialized,
        )

    def __on_player_proxy_initialized(self, proxy: DBusProxy) -> None:
        self.__player_proxy = proxy
        self.__player_proxy.gproxy.connect(
            "g-properties-changed", lambda *_: self.__sync_all()
        )

        self.__sync_all()
        self.__sync_position()
        self.connect("notify::metadata", lambda *_: self.__sync_metadata())
        self.emit("ready")

    def __sync_property(self, proxy: DBusProxy, py_name: str) -> None:
        def callback(value):
            if isinstance(value, GLib.Error):
                return

            if value == getattr(self, f"_{py_name}"):
                return

            setattr(self, f"_{py_name}", value)
            self.notify(py_name.replace("_", "-"))

        proxy.get_dbus_property_async(Utils.snake_to_pascal(py_name), callback=callback)

    def __sync_all(self) -> None:
        for prop_name in (
            "can_control",
            "can_go_next",
            "can_go_previous",
            "can_pause",
            "can_play",
            "can_seek",
            "loop_status",
            "metadata",
            "playback_status",
            "shuffle",
            "volume",
        ):
            self.__sync_property(self.__player_proxy, prop_name)

        for prop_name in (
            "identity",
            "desktop_entry",
        ):
            self.__sync_property(self.__mpris_proxy, prop_name)

    def __sync_metadata_property(
        self, key: str, py_name: str, custom_func: Callable | None = None
    ) -> None:
        prop = self.metadata.get(key, None)
        private_name = f"_{py_name}"
        if prop != getattr(self, private_name):
            if custom_func:
                setattr(self, private_name, custom_func(prop))
            else:
                setattr(self, private_name, prop)
            self.notify(py_name.replace("_", "-"))

    def __sync_metadata(self) -> None:
        # sync all properties that depend on metadata
        self.__sync_metadata_property("mpris:trackid", "track_id")
        self.__sync_metadata_property(
            "mpris:length",
            "length",
            lambda length: length // 1_000_000 if length else -1,
        )
        self.__sync_metadata_property("xesam:album", "album")
        self.__sync_metadata_property(
            "xesam:artist",
            "artist",
            lambda artist: "".join(artist) if isinstance(artist, list) else artist,
        )
        self.__sync_metadata_property("xesam:title", "title")
        self.__sync_metadata_property("xesam:url", "url")

        self.__cache_art_url()

    def __cache_art_url(self) -> None:
        def set_art_url(art_url: str | None) -> None:
            self._art_url = art_url
            self.notify("art-url")

        art_url = self.metadata.get("mpris:artUrl", None)

        if art_url == self._art_url:
            return

        if not art_url:  # string may be present but empty, so do not compare it to None
            set_art_url(None)
        else:
            self.__load_art_url(art_url, set_art_url)

    def __load_art_url(self, art_url: str, callback: Callable) -> None:
        path = ART_URL_CACHE_DIR + "/" + self.__get_valid_url_filename(art_url)
        if os.path.exists(path):
            callback(path)
            return

        def on_file_read(contents: bytes) -> None:
            Utils.write_file_async(
                path=path, contents=contents, callback=lambda: callback(path)
            )

        Utils.read_file_async(uri=art_url, decode=False, callback=on_file_read)

    def __get_valid_url_filename(self, url: str) -> str:
        parsed_url = urllib.parse.urlparse(url)

        domain = parsed_url.netloc.replace(".", "_")
        path = parsed_url.path.replace("/", "_")
        query = parsed_url.query.replace("&", "_").replace("=", "-")

        filename = f"{domain}{path}_{query}"

        return filename

    def __update_position(self) -> None:
        def callback(position: int | None) -> None:
            if isinstance(position, GLib.Error):
                return

            if position:
                self._position = position // 1_000_000
                self.notify("position")

        self.__player_proxy.get_dbus_property_async("Position", callback)

    def __sync_position(self) -> None:
        self.__update_position()
        Utils.Poll(1000, lambda *_: self.__update_position())

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
        return self._can_control

    @GObject.Property
    def can_go_next(self) -> bool:
        """
        - read-only

        Whether the player can go to the next track.
        """
        return self._can_go_next

    @GObject.Property
    def can_go_previous(self) -> bool:
        """
        - read-only

        Whether the player can go to the previous track.
        """
        return self._can_go_previous

    @GObject.Property
    def can_pause(self) -> bool:
        """
        - read-only

        Whether the player can pause.
        """
        return self._can_pause

    @GObject.Property
    def can_play(self) -> bool:
        """
        - read-only

        Whether the player can play.
        """
        return self._can_play

    @GObject.Property
    def can_seek(self) -> bool:
        """
        - read-only

        Whether the player can seek (change position on track in seconds).
        """
        return self._can_seek

    @GObject.Property
    def loop_status(self) -> str | None:
        """
        - read-only

        The current loop status.
        """
        return self._loop_status

    @GObject.Property
    def metadata(self) -> dict:
        """
        - read-only

        A dictionary containing metadata.
        """
        return self._metadata

    @GObject.Property
    def track_id(self) -> str | None:
        """
        - read-only

        The ID of the current track.
        """
        return self._track_id

    @GObject.Property
    def length(self) -> int:
        """
        - read-only

        The length of the current track,
        ``-1`` if not supported by the player.
        """
        return self._length

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
        return self._album

    @GObject.Property
    def artist(self) -> str | None:
        """
        - read-only

        The current artist name.
        """
        return self._artist

    @GObject.Property
    def title(self) -> str | None:
        """
        - read-only

        The current title of the track.
        """
        return self._title

    @GObject.Property
    def url(self) -> str | None:
        """
        - read-only

        The URL address of the track.
        """
        return self._url

    @GObject.Property
    def playback_status(self) -> str | None:
        """
        - read-only

        The current playback status. Can be "Playing" or "Paused".
        """
        return self._playback_status

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
        return self._shuffle

    @GObject.Property
    def volume(self) -> float:
        """
        - read-only

        The volume of the player.
        """
        return self._volume

    @GObject.Property
    def identity(self) -> str | None:
        """
        - read-only

        The name of the player (e.g. "Spotify", "firefox").
        """
        return self._identity

    @GObject.Property
    def desktop_entry(self) -> str | None:
        """
        - read-only

        The .desktop file of the player.
        """
        return self._desktop_entry

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
