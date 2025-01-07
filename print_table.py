"""
"""

from configuration import get_configuration, GAMES_KEY
from getpass import getpass

from databases import MariaDb
from databases.structs import get_db
from databases.structs._base import BaseDB
from games import get_game
from games.base_game import Game


if __name__ == "__main__":
    config = get_configuration()

    games: list[Game] = []
    for game_dict in config[GAMES_KEY].values():
        game_type = game_dict.pop('type')
        games.append(get_game(game_type, **game_dict))

    with MariaDb(host=config['database_host'], user=config["database_user"], password=config['database_pass'], database=config['database_name']) as db:
        for game in games:
            db_type = get_db(game.PLAYER_TYPE)
            db.print_table(BaseDB.ONLINE_TABLE_F.format(type(game).__name__.lower()))
