
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from players import BasePlayer


class Game:
    PLAYER_TYPE: type[BasePlayer]
    DEFAULT_PORT = 0

    def __init__(self, host: str, port: int = 0, password: str = "") -> None:
        self._log = logging.getLogger(__name__)

        assert self.DEFAULT_PORT != 0, "DEFAULT_PORT must be set in subclass."

        self.host = host
        self.port = port if port != 0 else self.DEFAULT_PORT
        self._pass = password

        if self.PLAYER_TYPE is None:
            raise ValueError("PLAYER_TYPE must be set in subclass.")

    def get_players(self) -> tuple[BasePlayer, ...]:
        """Get a list of players currently on the server.

        Returns:
            tuple[BasicPlayer, ...]: A list of online player names.
        """
        raise NotImplementedError

    def get_table_prefix(self) -> str:
        """Get the database table prefix for this game."""
        return f'{self.host}:{self.port}'
