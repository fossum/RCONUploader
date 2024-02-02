
from attr import define, field, validators


@define
class Player:
    name: str = field(validator=validators.instance_of(str))
    player_uid: int = field(validator=validators.instance_of(int))
    steam_id: int = field(validator=validators.instance_of(int))

    @staticmethod
    def parse_list(text: str) -> 'list[Player]':
        lines = text.splitlines()[1:]   # Toss header line.
        players = []
        for line in lines:
            if not line:
                continue
            name, uid, id = line.rsplit(',', maxsplit=2)
            players.append(Player(name, int(uid), int(id)))
        return players
