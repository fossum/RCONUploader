

from __future__ import annotations

from abc import ABC
import json
from typing import TYPE_CHECKING

from databases._base import sql_quote_list

if TYPE_CHECKING:
    from typing import Sequence

    from databases._base import DBBase
    from players import BasePlayer


class BaseDB(ABC):
    ONLINE_TABLE_F = '{}_online_players'
    KNOWN_PLAYERS_F = '{}_known_players'

    @staticmethod
    def insert_rows(database: DBBase, game: str, players: Sequence[BasePlayer]):
        raise NotImplementedError

    @staticmethod
    def ensure_db_struct(database: DBBase, database_name: str) -> bool:
        raise NotImplementedError

    @staticmethod
    def _common_insert_rows(database: DBBase, table_prefix: str, players: Sequence[BasePlayer], columns: Sequence[str], id_property: str):
        # Log current players into known table.
        insert_syntax = 'INSERT IGNORE INTO `{}` ({}) VALUES ({}) ON DUPLICATE KEY UPDATE `{}`="{}"'
        for player in players:
            database.execute(insert_syntax.format(
                BaseDB.KNOWN_PLAYERS_F.format(table_prefix),
                sql_quote_list(columns),
                f'"{getattr(player, id_property)}"',
                id_property,
                getattr(player, id_property)
            ))

        # Log currently online players.
        cursor = database.get_cursor()
        insert_syntax = f'INSERT INTO `{BaseDB.ONLINE_TABLE_F.format(table_prefix)}` (count, players) VALUES (%s, %s)'
        json_s = json.dumps([getattr(p, id_property) for p in players])
        cursor.execute(insert_syntax, [len(players), json_s])

        # Save the rows.
        database.execute("COMMIT")