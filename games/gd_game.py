
from __future__ import annotations

from logging import warning
import socket
from typing import TypedDict

import gamedig

from games.base_game import Game


class GDGame(Game):
    GAME_NAME: str

    class QueryArgs(TypedDict):
        game_id: str
        address: str
        port: int | None
        timeout_settings: gamedig.TimeoutSettings | None

    def __init_subclass__(cls, game_name: str):
        cls.GAME_NAME = game_name
        return super().__init_subclass__()

    @staticmethod
    def fqdn_to_ip(domain: str) -> str | None:
        ip_address = None
        try:
            ip_address = socket.gethostbyname(domain)
        except socket.gaierror:
            warning(f'Unable to get the IP address for {domain}')
        return ip_address

    def query(self) -> dict:
        kwargs: GDGame.QueryArgs = {
            "game_id": self.GAME_NAME,
            "address": self.fqdn_to_ip(self.host),
            "port": self.port if self.port else None,
            "timeout_settings": {
                "retries": 3,
            }
        }
        # if self._pass:
        #     kwargs["password"] = self._pass
        return gamedig.query(**kwargs)
