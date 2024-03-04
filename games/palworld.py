
from games.rcon_game import RCONGame
from players import BasePlayer, SteamPlayer


class Palworld(RCONGame, player_type=SteamPlayer):
    def get_players(self) -> list[BasePlayer]:
        # Get currently online players.
        players = Palworld._parse_list(self.send('ShowPlayers', enforce_id=False))
        self._log.info(f"Players Online: {', '.join([p.name for p in players])}")
        return players

    @staticmethod
    def _parse_list(text: str) -> 'list[SteamPlayer]':
        lines = text.splitlines()[1:]   # Toss header line.
        players = []
        for line in lines:
            if not line:
                continue
            name, uid, id = line.rsplit(',', maxsplit=2)
            players.append(SteamPlayer(name, int(uid), int(id)))
        return players
