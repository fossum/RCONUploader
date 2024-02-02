
import json
from pathlib import Path

from rcon.source import Client

from configuration import get_configuration
from databases import DBBase
from databases import MySQL
from players import Player

ONLINE_TABLE = 'online_players'
KNOWN_PLAYERS = 'known_players'


def mock_player_list() -> list[Player]:
    return Player.parse_list((Path(__file__).parent / 'test/showplayers_sample.txt').read_text())

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


def sql_quote_list(items: list[str]) -> str:
    return f"`{'`, `'.join(map(str, items))}`"


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

    # Get currently online players.
    # with Client(this_config['rcon_host'], this_config['rcon_port'], passwd=this_config['rcon_pass']) as client:
    #     players = Player.parse_list(client.run('ShowPlayers', enforce_id=False))
    #     # print(client.run('Save', enforce_id=False))
    players = mock_player_list()
    print(f"Players Online: {', '.join([p.name for p in players])}")

    with MySQL(this_config['database_host'], this_config['database_user'], this_config['database_pass']) as db:
        ensure_db_struct(db, this_config['database_name'])
        insert_rows(db, players)

        print("Tables:")
        mycursor = db._db.cursor()
        mycursor.execute("SHOW TABLES")
        for x in mycursor:
            print(f"\t{x}")

        print("Players:")
        mycursor = db._db.cursor()
        mycursor.execute(f"SELECT * FROM `{KNOWN_PLAYERS}`")
        for x in mycursor:
            print(f"\t{x}")

        print("Online:")
        mycursor = db._db.cursor()
        mycursor.execute(f"SELECT * FROM `{ONLINE_TABLE}`")
        for x in mycursor:
            print(f"\t{x}")
