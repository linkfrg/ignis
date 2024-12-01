from ignis.dbus import DBusProxy
from gi.repository import GObject  # type: ignore
from ignis.utils import Utils
from ignis.base_service import BaseService
from .player import MprisPlayer


class MprisService(BaseService):
    """
    A service for controlling media players using the MPRIS interface.

    Example usage:

    .. code-block:: python

        from ignis.services.mpris import MprisService

        mpris = MprisService.get_default()

        mpris.connect("player_added", lambda x, player: print(player.desktop_entry, player.title))
    """

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

    @GObject.Signal(arg_types=(MprisPlayer,))
    def player_added(self, *args):
        """
        - Signal

        Emitted when a player has been added.

        Args:
            player (:class:`~ignis.services.mpris.MprisPlayer`): The instance of the player.
        """
        pass

    @GObject.Property
    def players(self) -> list[MprisPlayer]:
        """
        - read-only

        A list of currently active players.
        """
        return list(self._players.values())
