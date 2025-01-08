"""Database Structure Creation Script.

This script creates a database and sets up user permissions using MySQL.
It prompts for admin credentials and uses configuration settings to:
1. Create a new database (if it doesn't exist)
2. Create a database user (if it doesn't exist)
3. Grant necessary permissions to the created user
Requirements:
    - MySQL server must be running and accessible
    - Admin credentials with sufficient privileges
    - Configuration file with database settings
Configuration needed:
    - database_host: MySQL server host address
    - database_name: Name of the database to create
    - database_user: Username to create/configure
    - database_pass: Password for the new user
Usage:
    python create_database_struct.py
Note:
    This script requires admin-level MySQL credentials to execute successfully.
    It will prompt for username and password during execution.
"""

from configuration import get_configuration
from getpass import getpass

from databases import MariaDb


if __name__ == "__main__":
    config = get_configuration()

    username = input("Enter username: ")
    password = getpass()

    with MariaDb(host=config['database_host'], user=username, password=password) as db:
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
