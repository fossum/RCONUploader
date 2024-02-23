
import logging

from rcon.source import Client

from players import Player


class RCONGame:
    def __init__(self, host, port, password) -> None:
        self._log = logging.getLogger(__name__)
        self._host = host
        self._port = port
        self._pass = password

    def get_players(self):
        # Get currently online players.
        with Client(self._host, self._port, passwd=self._pass) as client:
            players = Player.parse_list(client.run('ShowPlayers', enforce_id=False))
        self._log.info(f"Players Online: {', '.join([p.name for p in players])}")
        return players
