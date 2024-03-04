
from configuration import get_configuration
from getpass import getpass

from databases import MySQL


if __name__ == "__main__":
    config = get_configuration()

    username = input("Enter username: ")
    password = getpass()

    with MySQL(host=config['database_host'], user=username, password=password) as db:
        db.create_database(config['database_name'], if_not_exists=True)
        db.create_user(config['database_user'], config['database_pass'], if_not_exists=True)
        if db.execute(
                f"""
                    GRANT
                    SELECT, INSERT, UPDATE, DELETE,
                    CREATE, INDEX, DROP, ALTER, CREATE TEMPORARY TABLES, CREATE VIEW,
                    LOCK TABLES ON `{config['database_name']}`.* TO '{config['database_user']}'@'%'
                """) is None:
            raise RuntimeError
