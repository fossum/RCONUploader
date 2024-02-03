
from configuration import get_configuration
from databases import MySQL

ROOT_USER = 'root'
ROOT_PASS = 'password'
TABLE_NAME = 'online_players'

if __name__ == "__main__":
    config = get_configuration()

    with MySQL(host=config['database_host'], user=ROOT_USER, password=ROOT_PASS) as db:
        db.create_database(config['database_name'], if_not_exists=True)
        db.create_user(config['database_user'], config['database_pass'], if_not_exists=True)
        if db.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, INDEX, DROP, ALTER, CREATE TEMPORARY TABLES, LOCK TABLES ON `{config['database_name']}`.* TO '{config['database_user']}'@'%'") is None:
            raise RuntimeError
