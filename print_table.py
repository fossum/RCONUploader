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

    with MariaDb(host=config['database_host'], user=config["database_user"], password=config['database_pass'], database=config['database_name']) as db:
        for table_name in db.get_table_names():
            db.print_table(table_name)
