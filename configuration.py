
from configparser import ConfigParser
from os import getenv
from pathlib import Path
from typing import Any, Type

from attr import define


@define
class DBParam:
    name: str
    default_value: Any
    type: Type
    env_var: str
    config_section: str


@define
class GameParam:
    name: str
    default_value: Any
    type: Type


CONFIG_PATH = Path(__file__).parent / 'config.ini'
DATABASE_SECTION = 'DATABASE'
RCON_SECTION = 'RCON'
GAMES_KEY = 'GAMES'

DB_PARAMS = [
    DBParam('host', 'localhost', str, 'DB_HOST', DATABASE_SECTION),
    DBParam('port', '3306', int, 'DB_PORT', DATABASE_SECTION),
    DBParam('user', 'user', str, 'DB_USER', DATABASE_SECTION),
    DBParam('pass', 'password', str, 'DB_PASS', DATABASE_SECTION),
    DBParam('name', None, str, 'DB_NAME', DATABASE_SECTION),
]

GAME_PARAMS = [
    GameParam('type', '', str),
    GameParam('host', 'localhost', str),
    GameParam('port', '25575', int),
    GameParam('password', 'password', str),
]


def get_configuration() -> dict[str, str]:
    config = {}
    file_config = ConfigParser()
    file_config.read(str(CONFIG_PATH))

    def best_option(default=None, env_var=None, config_var=None):
        if config_var is not None:
            return config_var
        elif env_var is not None:
            return env_var
        elif default is not None:
            return default

        raise ValueError("No value set.")

    # Database
    for param in DB_PARAMS:
        option = f"{param.config_section}_{param.name}".lower()
        assert config.get(option) is None, f"Duplicate option '{option}' detected."

        # Check Config File
        config_var = None
        if file_config.has_section(param.config_section):
            config_var = file_config.get(param.config_section, param.name, fallback=None)

        config[option] = best_option(param.default_value, getenv(param.env_var), config_var)

        assert config[option], f'No configuration "{option}" value set.'
        config[option] = param.type(config[option])

    # Each Game Config
    for game in file_config.sections():
        if game == DATABASE_SECTION:
            continue

        if not config.get(GAMES_KEY):
            config[GAMES_KEY] = {}
        config[GAMES_KEY][game] = {}
        game_config = config[GAMES_KEY][game]

        for param in GAME_PARAMS:
            game_config[param.name] = param.type(
                best_option(
                    param.default_value,
                    None,
                    file_config.get(game, param.name, fallback=None)))

            assert game_config[param.name], f'No configuration "{param.name}" value set.'
            game_config[param.name] = param.type(game_config[param.name])

    return config
