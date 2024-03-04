
from attr import define, field, validators


@define
class BasePlayer:
    name: str = field(validator=validators.instance_of(str))


class SteamPlayer(BasePlayer):
    player_uid: int = field(validator=validators.instance_of(int))
    steam_id: int = field(validator=validators.instance_of(int))


class BasicPlayer(BasePlayer):
    name: str = field(validator=validators.instance_of(str))
