
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from players import BasePlayer


class Game:
    PLAYER_TYPE: type[BasePlayer]

    def __init__(self, host: str, port: int = 0, password: str = "") -> None:
        self._log = logging.getLogger(__name__)
        self.host = host
        self._port = port
        self._pass = password

        if self.PLAYER_TYPE is None:
            raise ValueError("PLAYER_TYPE must be set in subclass.")

    def get_players(self) -> tuple[BasePlayer, ...]:
        """Get a list of players currently on the server.

        Returns:
            tuple[BasicPlayer, ...]: A list of online player names.
        """
        raise NotImplementedError
