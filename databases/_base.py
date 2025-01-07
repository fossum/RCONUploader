
from abc import abstractmethod


class DBBase:

    @abstractmethod
    def __enter__(self):
        """Enters the context and opens/connects to the resource."""

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exits the context and closes the resource."""

    @abstractmethod
    def execute(self, command: str, ignore_error: bool = False) -> tuple[str]:
        raise NotImplementedError

    @abstractmethod
    def create_table(
            self,
            table_name: str,
            column_def: str,
            if_not_exists: bool = False,
            ignore_error: bool = False) -> bool:
        """Creates a table in the database."""

    @abstractmethod
    def create_database(
            self,
            name: str,
            options: str | None = None,
            if_not_exists: bool = False,
            ignore_error: bool = False) -> bool:
        """Creates a database in the server."""

    @abstractmethod
    def create_user(self, username: str, password: str, if_not_exists: bool = False):
        """Creates user"""

    @abstractmethod
    def database_exists(self, name) -> bool:
        """Tells you if a database exists in the server."""

    @abstractmethod
    def delete_database(self, name: str, ignore_error: bool = False) -> bool:
        """Deletes a database from the server."""


def sql_quote_list(items: list[str]) -> str:
    return f"`{'`, `'.join(map(str, items))}`"
