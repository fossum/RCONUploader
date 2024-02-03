
import mysql.connector
from mysql.connector.connection import MySQLConnection

from databases._base import DBBase


class MySQL(DBBase):

    def __init__(self, host, user, password, database: str | None = None):
        self._db = MySQLConnection(host=host, user=user, password=password, database=database)

    def __enter__(self) -> DBBase:
        self._db.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._db.close()

    def execute(self, command: str, ignore_error: bool = False) -> list[tuple] | None:
        cursor = self._db.cursor(buffered=True)
        try:
            cursor.execute(command)
        except mysql.connector.Error:
            if not ignore_error:
                raise
            return None
        ret = cursor.fetchall() if cursor.with_rows else []
        cursor.close()
        return ret

    def create_table(
            self,
            table_name: str,
            column_def: str,
            if_not_exists: bool = False,
            ignore_error: bool = False) -> bool:
        print(f"Creating table {table_name}")
        create_cmd_parts = ["CREATE", "TABLE"]
        if if_not_exists:
            create_cmd_parts.append("IF NOT EXISTS")
        create_cmd_parts.append(f"`{table_name}`")
        create_cmd_parts.append(f'({column_def})')
        return self.execute(' '.join(create_cmd_parts), ignore_error=ignore_error) is not None

    def create_database(
            self,
            name: str,
            options: str | None = None,
            if_not_exists: bool = False,
            ignore_error: bool = False) -> bool:
        print(f"Creating table {name}")
        create_cmd_parts = ["CREATE", "DATABASE"]
        if if_not_exists:
            create_cmd_parts.append("IF NOT EXISTS")
        create_cmd_parts.append(f"`{name}`")
        if options:
            create_cmd_parts.append(f'({options})')
        return self.execute(' '.join(create_cmd_parts), ignore_error=ignore_error) is not None

    def create_user(self, username: str, password: str, if_not_exists: bool = False):
        print(f"Creating user {username}")
        self.execute(f"CREATE USER {'IF NOT EXISTS' if if_not_exists else ''} '{username}'@'%' IDENTIFIED BY '{password}'")

    def database_exists(self, name) -> bool:
        print(f"Does database {name} exist? ", end='')
        cursor = self.execute("SHOW DATABASES")
        for row in cursor:
            if name == row[0]:
                print('yes.')
                return True
        print('no.')
        return False
