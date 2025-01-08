
from typing import Type

from databases.structs._base import BaseDB
from databases.structs.steam import SteamDB
from databases.structs.basic import BasicDB
from players import BasePlayer, BasicPlayer, SteamPlayer

_DB_MAP = {
    BasicPlayer: BasicDB,
    SteamPlayer: SteamDB
}


def get_db(player: Type[BasePlayer]) -> Type[BaseDB]:
    """Get the database type for a player type."""
    if (db_type := _DB_MAP.get(player)) is None:
        raise ValueError

    return db_type
