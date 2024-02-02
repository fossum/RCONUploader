
from configparser import ConfigParser
from os import getenv
from pathlib import Path
from typing import Any, Type

from attr import define


@define
class ConfigParam:
    name: str
    default_value: Any
    type: Type
    env_var: str
    config_section: str


CONFIG_PATH = Path(__file__).parent / 'config.ini'
DATABASE_SECTION = 'DATABASE'
RCON_SECTION = 'RCON'

PARAMS = [
    ConfigParam('host', 'localhost', str, 'DB_HOST', DATABASE_SECTION),
    ConfigParam('port', '3306', int, 'DB_PORT', DATABASE_SECTION),
    ConfigParam('user', 'user', str, 'DB_USER', DATABASE_SECTION),
    ConfigParam('pass', 'password', str, 'DB_PASS', DATABASE_SECTION),
    ConfigParam('name', None, str, 'DB_NAME', DATABASE_SECTION),

    ConfigParam('host', 'localhost', str, 'RCON_HOST', RCON_SECTION),
    ConfigParam('port', '25575', int, 'RCON_PORT', RCON_SECTION),
    ConfigParam('pass', 'password', str, 'RCON_PASS', RCON_SECTION),
]


def get_configuration() -> dict[str, str]:
    config = {}
    file_config = ConfigParser()
    file_config.read(str(CONFIG_PATH))

    for param in PARAMS:
        option = f"{param.config_section}_{param.name}".lower()
        assert config.get(option) is None, f"Duplicate option '{option}' detected."

        # Set default.
        config[option] = param.default_value

        # Check Environment Variable
        temp = getenv(param.env_var)
        if temp is not None:
            config[option] = temp

        # Check Config File
        if file_config.has_section(param.config_section):
            temp = file_config.get(param.config_section, param.name, fallback=None)
            if temp is not None:
                config[option] = temp

        assert config[option], f'No configuration "{option}" value set.'
        config[option] = param.type(config[option])

    return config
