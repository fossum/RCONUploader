

from __future__ import annotations
from typing import TYPE_CHECKING

from databases.structs._base import BaseDB

if TYPE_CHECKING:
    from typing import Sequence

    from databases._base import DBBase
    from players import BasePlayer



class SteamDB(BaseDB):
    @staticmethod
    def insert_rows(database: DBBase, table_prefix: str, players: Sequence[BasePlayer]) -> None:
        """Insert player data rows into the table."""
        SteamDB._common_insert_rows(database, table_prefix, players, ['steamId', 'uid', 'name'], 'steam_id')

    @staticmethod
    def ensure_db_struct(database: DBBase, table_prefix: str) -> bool:
        SteamDB._common_ensure_db_struct(
            database,
            table_prefix,
            [
                'steamId BIGINT UNSIGNED PRIMARY KEY',
                'uid BIGINT UNSIGNED',
                'name VARCHAR(32)'
            ]
        )
        return True

