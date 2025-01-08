
import logging
from time import sleep

from gamedig import AutoQueryError
import rcon.exceptions

from configuration import get_configuration, GAMES_KEY
from databases.structs import get_db
from databases import MariaDb
from games import get_game
from games.base_game import Game


if __name__ == "__main__":
    this_config = get_configuration()
    logging.basicConfig(
        level=logging.INFO
    )
    log = logging.getLogger()

    games: list[Game] = []
    for game_dict in this_config[GAMES_KEY].values():
        game_type = game_dict.pop('type')
        games.append(get_game(game_type, **game_dict))

    with MariaDb(
            this_config['database_host'],
            this_config['database_user'],
            this_config['database_pass'],
            this_config['database_name']) as db:
        for game in games:
            get_db(game.PLAYER_TYPE).ensure_db_struct(db, game.get_table_prefix())

    while True:
        try:
            with MariaDb(
                    this_config['database_host'],
                    this_config['database_user'],
                    this_config['database_pass'],
                    this_config['database_name']) as db:

                while True:
                    for game in games:
                        try:
                            get_db(game.PLAYER_TYPE).insert_rows(
                                db,
                                game.get_table_prefix(),
                                game.get_players()
                            )
                        except rcon.exceptions.EmptyResponse:
                            log.warning('No RCON response.')
                        except AutoQueryError as exc:
                            log.warning(f'[{game.host}] AutoQuery failed with error: %s', exc)
                    sleep(15)
        except ConnectionRefusedError:
            log.warning('MySQL Server down.')
