

from __future__ import annotations
import json
from typing import TYPE_CHECKING

from databases.structs._base import BaseDB
from databases._base import DBBase, sql_quote_list

if TYPE_CHECKING:
    from players import SteamPlayer


class SteamDB(BaseDB):
    @staticmethod
    def insert_rows(database: DBBase, game: str, players: list[SteamPlayer]):
        # Log current players into known table.
        insert_syntax = 'INSERT IGNORE INTO `{}` ({}) VALUES ({}) ON DUPLICATE KEY UPDATE `name`="{}"'
        for player in players:
            database.execute(insert_syntax.format(
                BaseDB.KNOWN_PLAYERS_F.format(game),
                sql_quote_list(['steamId', 'uid', 'name']),
                ', '.join([str(player.steam_id), str(player.player_uid), f'"{player.name}"']),
                player.name
            ))

        # Log currently online players.
        cursor = database._db.cursor()
        insert_syntax = f'INSERT INTO `{BaseDB.ONLINE_TABLE_F.format(game)}` (count, players) VALUES (%s, %s)'
        json_s = json.dumps([p.steam_id for p in players])
        cursor.execute(insert_syntax, [len(players), json_s])

        # Save the rows.
        database.execute("COMMIT")

    @staticmethod
    def ensure_db_struct(database: DBBase, game: str) -> bool:
        # # Connect to uploader database.
        # if not database.database_exists(database_name):
        #     raise RuntimeError('No database or missing privelegdes.')
        # database._db.connect(database=database_name)

        # Ensure table structure.
        database.create_table(
            BaseDB.ONLINE_TABLE_F.format(game),
            '''
                id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                count TINYINT UNSIGNED,
                players JSON
            ''',
            if_not_exists=True)
        database.create_table(
            BaseDB.KNOWN_PLAYERS_F.format(game),
            '''
                steamId BIGINT UNSIGNED PRIMARY KEY,
                uid BIGINT UNSIGNED,
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

