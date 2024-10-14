from ignis.dbus import DBusProxy
from gi.repository import GObject  # type: ignore
from ignis.utils import Utils
from ignis.base_service import BaseService
from .player import MprisPlayer


class MprisService(BaseService):
    """
    Service for getting and controlling media players using the MPRIS interface (e.g., Spotify, Firefox/Chromium with playing media).

    **Dependencies:**
        - **python-requests**

    Signals:
        - **"player_added"** (:class:`~ignis.services.applications.Application`): Emitted when a :class:`~ignis.services.applications.Application` has been added.

    Properties:
        - **players** (list[:class:`~ignis.services.applications.Application`], read-only): A list of currently active players.

    **Example usage:**

    .. code-block:: python

        from ignis.services.mpris import MprisService

        mpris = MprisService.get_default()

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
        self._players: dict[str, MprisPlayer] = {}

        self.__dbus = DBusProxy(
            name="org.freedesktop.DBus",
            object_path="/org/freedesktop/DBus",
            interface_name="org.freedesktop.DBus",
            info=Utils.load_interface_xml("org.freedesktop.DBus"),
        )

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
            and name not in self._players
            and name != "org.mpris.MediaPlayer2.playerctld"
        ):
            player = MprisPlayer(name)
            player.connect("ready", self.__add_player, name)

    def __add_player(self, player: MprisPlayer, name: str) -> None:
        self._players[name] = player
        player.connect("closed", lambda x: self.__remove_player(name))
        self.emit("player_added", player)
        self.notify("players")

    def __remove_player(self, name: str) -> None:
        if name in self._players:
            self._players.pop(name)
            self.notify("players")

    @GObject.Property
    def players(self) -> list[MprisPlayer]:
        return list(self._players.values())
