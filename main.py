
import json
import logging
from pathlib import Path
from time import sleep

import rcon.exceptions
from rcon.source import Client

from configuration import get_configuration
from databases import DBBase
from databases import MySQL
from players import Player

ONLINE_TABLE = 'online_players'
KNOWN_PLAYERS = 'known_players'


def ensure_db_struct(database: DBBase, database_name: str) -> bool:
    # Connect to game database.
    if not database.database_exists(database_name):
        raise RuntimeError('No database or missing privelegdes.')
    database._db.connect(database=database_name)

    # Ensure table structure.
    database.create_table(
        ONLINE_TABLE,
        'id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, count TINYINT UNSIGNED, players JSON',
        if_not_exists=True)
    database.create_table(
        KNOWN_PLAYERS,
        'steamId BIGINT UNSIGNED PRIMARY KEY, uid BIGINT UNSIGNED, name VARCHAR(32)',
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


def get_players():
    # Get currently online players.
    with Client(this_config['rcon_host'], this_config['rcon_port'], passwd=this_config['rcon_pass']) as client:
        players = Player.parse_list(client.run('ShowPlayers', enforce_id=False))
    # players = mock_player_list()
    log.info(f"Players Online: {', '.join([p.name for p in players])}")
    return players


def insert_rows(database: DBBase, players: list[Player]):
    # Log current players into known table.
    insert_syntax = 'INSERT IGNORE INTO `{}` ({}) VALUES ({}) ON DUPLICATE KEY UPDATE `name`="{}"'
    for player in players:
        database.execute(insert_syntax.format(
            KNOWN_PLAYERS,
            sql_quote_list(['steamId', 'uid', 'name']),
            ', '.join([str(player.steam_id), str(player.player_uid), f'"{player.name}"']),
            player.name
        ))

    # Log currently online players.
    cursor = database._db.cursor()
    insert_syntax = f'INSERT INTO `{ONLINE_TABLE}` (count, players) VALUES (%s, %s)'
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

    while True:
        try:
            with MySQL(
                    this_config['database_host'],
                    this_config['database_user'],
                    this_config['database_pass'],
                    this_config['database_name']) as db:
                ensure_db_struct(db, this_config['database_name'])

                while True:
                    try:
                        insert_rows(db, get_players())
                    except rcon.exceptions.EmptyResponse:
                        log.warning('No RCON response.')
                    sleep(30)
        except ConnectionRefusedError:
            log.warning('MySQL Server down.')
