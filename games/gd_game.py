
from __future__ import annotations

from logging import warn, warning
import socket

import gamedig

from games.base_game import Game


class GDGame(Game):
    GAME_NAME: str

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
        kwargs = {
            "game_id": self.GAME_NAME,
            "address": self.fqdn_to_ip(self.host)
        }
        if self._port:
            kwargs["port"] = self._port
        # if self._pass:
        #     kwargs["password"] = self._pass
        return gamedig.query(**kwargs)
