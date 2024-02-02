
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

    def database_exists(self, name) -> bool:
        print(f"Does database {name} exist? ", end='')
        cursor = self.execute("SHOW DATABASES")
        for row in cursor:
            if name == row[0]:
                print('yes.')
                return True
        print('no.')
        return False




# database='mydatabase'
# user='root'
# # user='user'
# password='password'
# with MySQL(host='db', user=user, password=password, database=database) as my:

#     my.database_exists('palworld')
#     my.database_exists('palworld2')
#     my.create_database('palworld', if_not_exists=True)
#     my.create_table('t2', '`emp_no` int(11) NOT NULL', if_not_exists=True)

#     mycursor = my._db.cursor()
#     mycursor.execute("SHOW DATABASES")
#     for x in mycursor:
#         print(x)

#     mycursor.execute("SHOW TABLES")
#     for x in mycursor:
#         print(x)
