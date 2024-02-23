
# Base First
from typing import Type
from games.rcon_game import RCONGame

# Games
from games.palworld import Palworld

GAME_MAPPING: dict[str, Type[RCONGame]] = {
    'palworld': Palworld
}


def get_game(type: str, *args, **kwargs) -> RCONGame:
    game_type = GAME_MAPPING.get(type.lower())

    if game_type is None:
        raise ValueError(f"No game type known for {type}")

    return game_type(*args, **kwargs)
