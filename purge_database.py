"""
"""

from configuration import get_configuration
from getpass import getpass

from databases import MariaDb


if __name__ == "__main__":
    config = get_configuration()

    username = input("Enter database admin username: ")
    password = getpass()

    with MariaDb(host=config['database_host'], user=username, password=password) as db:
        db.delete_database(config['database_name'], ignore_error=True)
