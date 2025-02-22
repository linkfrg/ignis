import os
import asyncio
from ignis.dbus import DBusProxy
from gi.repository import GObject, GLib  # type: ignore
from ignis.gobject import IgnisGObject
from ignis.utils import Utils
from collections.abc import Callable
from .constants import ART_URL_CACHE_DIR
from .util import uri_to_unix_path


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

        asyncio.create_task(self.__init_proxy(name))

    async def __init_proxy(self, name: str) -> None:
        self.__mpris_proxy = await DBusProxy.new_async(
            name=name,
            object_path="/org/mpris/MediaPlayer2",
            interface_name="org.mpris.MediaPlayer2",
            info=Utils.load_interface_xml("org.mpris.MediaPlayer2"),
        )

        self.__player_proxy = await DBusProxy.new_async(
            name=self.__mpris_proxy.name,
            object_path=self.__mpris_proxy.object_path,
            interface_name="org.mpris.MediaPlayer2.Player",
            info=Utils.load_interface_xml("org.mpris.MediaPlayer2.Player"),
        )

        self.__mpris_proxy.watch_name(
            on_name_vanished=lambda *args: self.emit("closed")
        )

        asyncio.create_task(self.__sync_position())
        await self.__sync_all()
        await self.__sync_metadata()
        await self.__update_position()

        self.__player_proxy.gproxy.connect(
            "g-properties-changed", lambda *_: asyncio.create_task(self.__sync_all())
        )
        self.connect(
            "notify::metadata", lambda *_: asyncio.create_task(self.__sync_metadata())
        )

        self.emit("ready")

    async def __sync_property(self, proxy: DBusProxy, py_name: str) -> None:
        try:
            value = await proxy.get_dbus_property_async(Utils.snake_to_pascal(py_name))
        except GLib.Error:
            return

        if value == getattr(self, f"_{py_name}"):
            return

        setattr(self, f"_{py_name}", value)
        self.notify(py_name.replace("_", "-"))

    async def __sync_all(self) -> None:
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
            await self.__sync_property(self.__player_proxy, prop_name)

        for prop_name in (
            "identity",
            "desktop_entry",
        ):
            await self.__sync_property(self.__mpris_proxy, prop_name)

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

    async def __sync_metadata(self) -> None:
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
        await self.__cache_art_url()

    async def __cache_art_url(self) -> None:
        art_url = self.metadata.get("mpris:artUrl", None)
        result = None

        if art_url == self._art_url:
            return

        if art_url:
            result = await self.__load_art_url(art_url)

        self._art_url = result
        self.notify("art_url")

    async def __load_art_url(self, art_url: str) -> str:
        path = ART_URL_CACHE_DIR + "/" + uri_to_unix_path(art_url)
        if os.path.exists(path):
            return path

        contents = await Utils.read_file_async(uri=art_url, decode=False)
        await Utils.write_file_async(path=path, contents=contents)  # type: ignore
        return path

    async def __update_position(self) -> None:
        try:
            position = await self.__player_proxy.get_dbus_property_async("Position")
        except GLib.Error:
            return
        if position:
            self._position = position // 1_000_000
            self.notify("position")

    async def __sync_position(self) -> None:
        while True:
            await self.__update_position()
            await asyncio.sleep(1)

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
