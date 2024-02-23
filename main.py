
import json
import logging
from time import sleep

import rcon.exceptions

from configuration import get_configuration, GAMES_KEY
from databases import DBBase
from databases import MySQL
from games import get_game
from players import Player

ONLINE_TABLE = '{}_online_players'
KNOWN_PLAYERS = '{}_known_players'


def ensure_db_struct(database: DBBase, database_name: str) -> bool:
    # Connect to uploader database.
    if not database.database_exists(database_name):
        raise RuntimeError('No database or missing privelegdes.')
    database._db.connect(database=database_name)

    # Ensure table structure.
    database.create_table(
        ONLINE_TABLE.format(database),
        '''
            id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            count TINYINT UNSIGNED,
            players JSON
        ''',
        if_not_exists=True)
    database.create_table(
        KNOWN_PLAYERS.format(database),
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


def sql_quote_list(items: list[str]) -> str:
    return f"`{'`, `'.join(map(str, items))}`"


def insert_rows(database: DBBase, game: str, players: list[Player]):
    # Log current players into known table.
    insert_syntax = 'INSERT IGNORE INTO `{}` ({}) VALUES ({}) ON DUPLICATE KEY UPDATE `name`="{}"'
    for player in players:
        database.execute(insert_syntax.format(
            KNOWN_PLAYERS.format(game),
            sql_quote_list(['steamId', 'uid', 'name']),
            ', '.join([str(player.steam_id), str(player.player_uid), f'"{player.name}"']),
            player.name
        ))

    # Log currently online players.
    cursor = database._db.cursor()
    insert_syntax = f'INSERT INTO `{ONLINE_TABLE.format(game)}` (count, players) VALUES (%s, %s)'
    json_s = json.dumps([p.steam_id for p in players])
    cursor.execute(insert_syntax, [len(players), json_s])

    # Save the rows.
    database.execute("COMMIT")


if __name__ == "__main__":
    this_config = get_configuration()
    logging.basicConfig(
        level=logging.INFO
    )
    log = logging.getLogger()

    games = []
    for game_dict in this_config[GAMES_KEY].values():
        game_type = game_dict.pop('type')
        games.append(get_game(game_type, **game_dict))

    with MySQL(
            this_config['database_host'],
            this_config['database_user'],
            this_config['database_pass'],
            this_config['database_name']) as db:
        ensure_db_struct(db, this_config['database_name'])

    while True:
        try:
            with MySQL(
                    this_config['database_host'],
                    this_config['database_user'],
                    this_config['database_pass'],
                    this_config['database_name']) as db:

                while True:
                    for game in this_config[GAMES_KEY]:
                        try:
                            insert_rows(db, game.get_players())
                        except rcon.exceptions.EmptyResponse:
                            log.warning('No RCON response.')
                    sleep(30)
        except ConnectionRefusedError:
            log.warning('MySQL Server down.')
