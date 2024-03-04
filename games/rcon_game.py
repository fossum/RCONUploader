
from __future__ import annotations
import logging
from typing import TYPE_CHECKING

from rcon.source import Client

if TYPE_CHECKING:
    from players import BasePlayer


class RCONGame:
    PLAYER_TYPE: BasePlayer

    def __init__(self, host: str, port, password: str) -> None:
        if not getattr(self, '_log'):
            self._log = logging.getLogger(__name__)
        self._host = host
        self._port = port
        self._pass = password

    def __init_subclass__(cls, player_type: BasePlayer) -> None:
        cls._log = logging.getLogger(cls.__module__)
        cls.PLAYER_TYPE = player_type
        return super().__init_subclass__()

    def get_players(self) -> list[BasePlayer]:
        raise NotImplementedError

    def send(self, msg: str, enforce_id: bool = True) -> str:
        with Client(self._host, self._port, passwd=self._pass) as client:
            return client.run(msg, enforce_id=enforce_id)
