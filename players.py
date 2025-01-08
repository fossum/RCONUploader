
from attr import define, field, validators


@define
class BasePlayer:
    """A basic player with only a name."""
    name: str = field(validator=validators.instance_of(str))


@define
class SteamPlayer(BasePlayer):
    """A player with a Steam ID."""
    player_uid: int = field(validator=validators.instance_of(int))
    steam_id: int = field(validator=validators.instance_of(int))


@define
class BasicPlayer(BasePlayer):
    pass
