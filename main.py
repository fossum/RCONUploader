
import json
import logging
from time import sleep

import rcon.exceptions

from configuration import get_configuration, GAMES_KEY
from databases import DBBase
from databases.structs import get_db
from databases import MySQL
from games import get_game
from players import SteamPlayer


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
        for game in games:
            get_db(game.PLAYER_TYPE).ensure_db_struct(db, type(game).__name__.lower())

    while True:
        try:
            with MySQL(
                    this_config['database_host'],
                    this_config['database_user'],
                    this_config['database_pass'],
                    this_config['database_name']) as db:

                while True:
                    for game in games:
                        try:
                            get_db(game.PLAYER_TYPE).insert_rows(db, type(game).__name__.lower(), game.get_players())
                        except rcon.exceptions.EmptyResponse:
                            log.warning('No RCON response.')
                    sleep(5)
        except ConnectionRefusedError:
            log.warning('MySQL Server down.')
