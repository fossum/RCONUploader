
# Base First
from typing import Type
from games.base_game import Game
from games.rcon_game import RCONGame

# Games
from games.palworld import Palworld
from games.minecraft import Minecraft
from games.valheim import Valheim

GAME_MAPPING: dict[str, Type[Game]] = {
    'palworld': Palworld,
    'minecraft': Minecraft,
    'valheim': Valheim
}


def get_game(type: str, *args, **kwargs) -> Game:
    game_type = GAME_MAPPING.get(type.lower())

    if game_type is None:
        raise ValueError(f"No game type known for {type}")

    return game_type(*args, **kwargs)
