
from __future__ import annotations

from games.base_game import Game
from rcon.source import Client


class RCONGame(Game):
    def send(self, msg: str, enforce_id: bool = True) -> str:
        with Client(self._host, self._port, passwd=self._pass) as client:
            return client.run(msg, enforce_id=enforce_id)
