

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from databases.structs._base import BaseDB
from databases._base import DBBase, sql_quote_list

if TYPE_CHECKING:
    from typing import Sequence

    from players import BasicPlayer


class BasicDB(BaseDB):
    @staticmethod
    def insert_rows(database: DBBase, table_prefix: str, players: Sequence[BasicPlayer]):
        # Log current players into known table.
        insert_syntax = 'INSERT IGNORE INTO `{}` ({}) VALUES ({}) ON DUPLICATE KEY UPDATE `name`="{}"'
        for player in players:
            # assert isinstance(player, BasicPlayer)
            database.execute(insert_syntax.format(
                BaseDB.KNOWN_PLAYERS_F.format(table_prefix),
                sql_quote_list(['name']),
                f'"{player.name}"',
                player.name
            ))

        # Log currently online players.
        cursor = database.get_cursor()
        insert_syntax = f'INSERT INTO `{BaseDB.ONLINE_TABLE_F.format(table_prefix)}` (count, players) VALUES (%s, %s)'
        json_s = json.dumps([p.name for p in players])
        cursor.execute(insert_syntax, [len(players), json_s])

        # Save the rows.
        database.execute("COMMIT")

    @staticmethod
    def ensure_db_struct(database: DBBase, table_prefix: str) -> bool:
        # # Connect to uploader database.
        # if not database.database_exists(database_name):
        #     raise RuntimeError('No database or missing privelegdes.')
        # database._db.connect(database=database_name)

        # Ensure table structure.
        database.create_table(
            BaseDB.ONLINE_TABLE_F.format(table_prefix),
            '''
                id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                count TINYINT UNSIGNED,
                players JSON
            ''',
            if_not_exists=True)
        database.create_table(
            BaseDB.KNOWN_PLAYERS_F.format(table_prefix),
            '''
                name VARCHAR(32)
            ''',
            if_not_exists=True)

        # Create Views
        # CREATE OR REPLACE VIEW `palworld`.`OnlinePlayers` AS SELECT `name` FROM `known_players` where JSON_CONTAINS((SELECT `players` FROM `online_players` ORDER BY id DESC LIMIT 1), `steamId`);
        # database.execute(
        #     """
        #         CREATE OR REPLACE
        #         VIEW OnlinePlayers AS
        #         SELECT `name`
        #         FROM `known_players`
        #         where JSON_CONTAINS(
        #             (SELECT `players` FROM `online_players` ORDER BY id DESC LIMIT 1),
        #             `steamId`)
        #     """
        # )
        return True

