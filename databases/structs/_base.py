

from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from databases._base import DBBase
    from players import BasicPlayer


class BaseDB(ABC):
    ONLINE_TABLE_F = '{}_online_players'
    KNOWN_PLAYERS_F = '{}_known_players'

    @staticmethod
    def insert_rows(database: DBBase, game: str, players: list[BasicPlayer]):
        raise NotImplementedError

    @staticmethod
    def ensure_db_struct(database: DBBase, database_name: str) -> bool:
        raise NotImplementedError
