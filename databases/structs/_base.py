

from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from databases._base import DBBase
    from players import BasePlayer


class BaseDB(ABC):
    ONLINE_TABLE_F = '{}_online_players'
    KNOWN_PLAYERS_F = '{}_known_players'

    def insert_rows(database: DBBase, game: str, players: list[BasePlayer]):
        pass

    def ensure_db_struct(database: DBBase, database_name: str) -> bool:
        pass
