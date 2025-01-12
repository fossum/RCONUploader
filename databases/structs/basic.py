

from __future__ import annotations

from typing import TYPE_CHECKING

from databases.structs._base import BaseDB
from databases._base import DBBase

if TYPE_CHECKING:
    from typing import Sequence

    from players import BasePlayer


class BasicDB(BaseDB):
    @staticmethod
    def insert_rows(database: DBBase, table_prefix: str, players: Sequence[BasePlayer]):
        """Insert player rows into the database table."""
        BasicDB._common_insert_rows(database, table_prefix, players, ['name'], 'name')

    @staticmethod
    def ensure_db_struct(database: DBBase, table_prefix: str) -> bool:
        BasicDB._common_ensure_db_struct(database, table_prefix, ['name VARCHAR(32)'])
        return True
