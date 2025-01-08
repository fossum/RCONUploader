
import mariadb

from databases._base import DBBase


class MariaDb(DBBase):

    def __init__(self, host, user, password, database: str | None = None) -> None:
        self._db = None
        self._host = host
        self._user = user
        self._password = password
        self._database_name = database

    def __enter__(self) -> DBBase:
        self._db = mariadb.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            database=self._database_name
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._db is not None:
            self._db.close()

    def execute(self, command: str, ignore_error: bool = False) -> tuple[str]:
        cursor = self.get_cursor()
        try:
            cursor.execute(command)
            if command.strip().upper().startswith(('SELECT', 'SHOW')):
                ret = tuple(cursor.fetchall())
            else:
                assert self._db is not None, "Database not connected."
                self._db.commit()
                ret = ()
        except mariadb.Error:
            if not ignore_error:
                raise
            return ()
        finally:
            cursor.close()
        return tuple(ret)

    def get_cursor(self):
        return self._db.cursor(buffered=True)

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
        if cursor is not None:
            for row in cursor:
                if name == row[0]:
                    print('yes.')
                    return True
        print('no.')
        return False

    def delete_database(self, name: str, ignore_error: bool = False) -> bool:
        print(f"Deleting database {name}")
        return self.execute(f"DROP DATABASE {name}", ignore_error=ignore_error) is not None

    def print_table(self, table_name: str | None = None) -> None:
        """Prints the contents of the table."""
        print(f"Rows in table {self._database_name}.{table_name}:")
        cursor = self.execute(f"SELECT * FROM `{table_name}` LIMIT 10")
        if cursor is not None:
            for row in cursor:
                print(row)

    def get_table_names(self) -> tuple[str, ...]:
        """Get a list of table names in the database."""
        cursor = self.execute("SHOW TABLES")
        if cursor is not None:
            return tuple(row[0] for row in cursor)
        return ()
