import shutil
import os
import time
from ignis.dbus import DBusProxy
from gi.repository import GObject, GLib
from ignis.gobject import IgnisGObject
from ignis.utils import Utils
from ignis.logging import logger
from typing import List
from ignis.settings import CACHE_DIR

ART_URL_CACHE_DIR = f"{CACHE_DIR}/art_url"

os.makedirs(ART_URL_CACHE_DIR, exist_ok=True)

class RequestsModuleNotFoundError(Exception):
    """
    Raised when the Python requests module is not found.
    """
    def __init__(self, *args: object) -> None:
        super().__init__("Requests module not found! To use the audio service, install python-requests", *args)

try:
    import requests
except (ImportError, ValueError):
    raise RequestsModuleNotFoundError() from None


class MprisPlayer(IgnisGObject):
    """
    A media player object.

    Signals:
        - **"closed"** (): Emitted when a player has been closed or removed.

    Properties:
        - **can_control** (``bool``, read-only): Whether the player can be controlled.
        - **can_go_next** (``bool``, read-only): Whether the player can go to the next track.
        - **can_go_previous** (``bool``, read-only): Whether the player can go to the previous track.
        - **can_pause** (``bool``, read-only): Whether the player can pause.
        - **can_play** (``bool``, read-only): Whether the player can play.
        - **can_seek** (``bool``, read-only): Whether the player can seek (change position on track in seconds).
        - **loop_status** (``str``, read-only): Loop status.
        - **metadata** (``dict``, read-only): Dictionary containing metadata. You typically shouldn't use this property.
        - **track_id** (``str``, read-only): Track ID.
        - **length** (``int``, read-only): Length of media. Returns -1 if not supported by player.
        - **art_url** (``str``, read-only): Path to cached art image of media.
        - **album** (``str``, read-only): Album name.
        - **artist** (``str``, read-only): Artist name.
        - **title** (``str``, read-only): Current title.
        - **url** (``str``, read-only): URL address to the media.
        - **playback_status** (``str``, read-only): Playback status. Can be "Playing" or "Paused".
        - **position** (``position``, read-write): Current position in the track, in seconds.
        - **shuffle** (``bool``, read-only): Shuffle status (honestly idk what is that).
        - **volume** (``float``, read-only): Player volume.
        - **identity** (``bool``, read-only): Name of the player (e.g. "Spotify", "firefox").
        - **desktop_entry** (``bool``, read-only): .desktop file of the player.

    """

    __gsignals__ = {
        "ready": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
        "closed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, name: str):
        super().__init__()
        self._position = -1
        self._art_url = None

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

        self.__mpris_proxy.proxy.connect(
            "notify::g-name-owner", lambda *args: self.emit("closed")
        )

        self.__ready()

    @Utils.run_in_thread
    def __ready(self) -> None:
        self.__sync_position()
        self.__cache_art_url()
        self.emit("ready")

    def __sync(self, proxy, properties: GLib.Variant, invalidated_properties) -> None:
        prop_dict = properties.unpack()
        for key in prop_dict.keys():
            if key == "Metadata":
                self.__cache_art_url()

        self.notify_all()

    @Utils.run_in_thread
    def __cache_art_url(self) -> None:
        art_url = self.metadata.get("mpris:artUrl", None)
        if not art_url:
            return

        if art_url.startswith("file://"):
            path = art_url.replace("file://", "")
            result = ART_URL_CACHE_DIR + "/" + os.path.basename(path)
            if not os.path.exists(result):
                shutil.copy(path, result)

        elif art_url.startswith("https://") or art_url.startswith("http://"):
            result = ART_URL_CACHE_DIR + "/" + os.path.basename(art_url)
            if not os.path.exists(result):
                try:
                    response = requests.get(art_url)
                except requests.exceptions.ConnectionError:
                    logger.warning("Failed to download the art image of media.")
                    return

                if response.status_code == 200:
                    with open(
                        os.path.join(ART_URL_CACHE_DIR, os.path.basename(art_url)),
                        "wb",
                    ) as file:
                        file.write(response.content)
                else:
                    logger.warning("Failed to download the art image of media.")

        self._art_url = result
        self.notify("art_url")

    @Utils.run_in_thread
    def __sync_position(self) -> None:
        while True:
            position = self.__player_proxy.Position
            if position:
                self._position = position // 1_000_000
                self.notify("position")
            time.sleep(1)

    @GObject.Property
    def can_control(self) -> bool:
        return self.__player_proxy.CanControl

    @GObject.Property
    def can_go_next(self) -> bool:
        return self.__player_proxy.CanGoNext

    @GObject.Property
    def can_go_previous(self) -> bool:
        return self.__player_proxy.CanGoPrevious

    @GObject.Property
    def can_pause(self) -> bool:
        return self.__player_proxy.CanPause

    @GObject.Property
    def can_play(self) -> bool:
        return self.__player_proxy.CanPlay

    @GObject.Property
    def can_seek(self) -> bool:
        return self.__player_proxy.CanSeek

    @GObject.Property
    def loop_status(self) -> str:
        return self.__player_proxy.LoopStatus

    @GObject.Property
    def metadata(self) -> dict:
        metadata = getattr(self.__player_proxy, "Metadata", None)
        if metadata:
            return metadata
        else:
            return {}

    @GObject.Property
    def track_id(self) -> str:
        return self.metadata.get("mpris:trackid", None)

    @GObject.Property
    def length(self) -> int:
        length = self.metadata.get("mpris:length", None)
        if length:
            return length // 1_000_000
        else:
            return -1

    @GObject.Property
    def art_url(self) -> str:
        return self._art_url

    @GObject.Property
    def album(self) -> str:
        return self.metadata.get("xesam:album", None)

    @GObject.Property
    def artist(self) -> str:
        artist = self.metadata.get("xesam:artist", None)
        if isinstance(artist, list):
            return "".join(artist)
        else:
            return artist

    @GObject.Property
    def title(self) -> str:
        return self.metadata.get("xesam:title", None)

    @GObject.Property
    def url(self) -> str:
        return self.metadata.get("xesam:url", None)

    @GObject.Property
    def playback_status(self) -> str:
        return self.__player_proxy.PlaybackStatus

    @GObject.Property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, value: int) -> None:
        self.__player_proxy.SetPosition("(ox)", self.track_id, value * 1_000_000)

    def set_position(self, value: int) -> None:
        self.position = value

    @GObject.Property
    def shuffle(self) -> bool:
        return self.__player_proxy.Shuffle

    @GObject.Property
    def volume(self) -> float:
        return self.__player_proxy.Volume

    @GObject.Property
    def identity(self) -> str:
        return self.__mpris_proxy.Identity

    @GObject.Property
    def desktop_entry(self) -> str:
        return self.__mpris_proxy.DesktopEntry

    def next(self) -> None:
        """
        Go to the next track.
        """
        self.__player_proxy.Next()

    def previous(self) -> None:
        """
        Go to the previous track.
        """
        self.__player_proxy.Previous()

    def pause(self) -> None:
        """
        Pause playback.
        """
        self.__player_proxy.Pause()

    def play(self) -> None:
        """
        Start playback.
        """
        self.__player_proxy.Play()

    def play_pause(self) -> None:
        """
        Toggle between playing and pausing.
        """
        self.__player_proxy.PlayPause()

    def stop(self) -> None:
        """
        Stop playback and remove the MPRIS interface if supported by the player.
        """
        self.__player_proxy.Stop()

    def seek(self, offset: int) -> None:
        """
        Seek to a specific position in the track.
        Positive values move forward, and negative values move backward.
        The offset is in milliseconds.
        """
        self.__player_proxy.Seek("(x)", offset * 1_000_100)


class MprisService(IgnisGObject):
    """
    Service for getting and controlling media players using the MPRIS interface (e.g., Spotify, Firefox/Chromium with playing media).

    **Dependencies:**
        - **python-requests**

    Signals:
        - **"player_added"** (:class:`~ignis.services.applications.Application`): Emitted when a :class:`~ignis.services.applications.Application` has been added.

    Properties:
        - **players** (List[:class:`~ignis.services.applications.Application`], read-only): List of currently active players.

    .. code-block:: python

        from ignis.service import Service

        mpris = Service.get("mpris")

        mpris.connect("player_added", lambda x, player: print(player.desktop_entry, player.title))
    """

    __gsignals__ = {
        "player_added": (
            GObject.SignalFlags.RUN_FIRST,
            GObject.TYPE_NONE,
            (GObject.Object,),
        ),
    }

    def __init__(self):
        super().__init__()
        self.__dbus = DBusProxy(
            name="org.freedesktop.DBus",
            object_path="/org/freedesktop/DBus",
            interface_name="org.freedesktop.DBus",
            info=Utils.load_interface_xml("org.freedesktop.DBus"),
        )
        self.__players = {}

        self.__dbus.signal_subscribe(
            signal_name="NameOwnerChanged",
            callback=lambda *args: self.__init_player(args[5][0]),
        )

        self.__get_players()

    def __get_players(self) -> None:
        all_names = self.__dbus.ListNames()
        for name in all_names:
            self.__init_player(name)

    def __init_player(self, name: str) -> None:
        if (
            name.startswith("org.mpris.MediaPlayer2")
            and name not in self.__players
            and name != "org.mpris.MediaPlayer2.playerctld"
        ):
            player = MprisPlayer(name)
            player.connect("ready", self.__add_player, name)

    def __add_player(self, player: MprisPlayer, name: str) -> None:
        self.__players[name] = player
        player.connect("closed", lambda x: self.__remove_player(name))
        self.emit("player_added", player)
        self.notify("players")

    def __remove_player(self, name: str) -> None:
        if name in self.__players:
            self.__players.pop(name)
            self.notify("players")

    @GObject.Property
    def players(self) -> List[MprisPlayer]:
        return list(self.__players.values())
