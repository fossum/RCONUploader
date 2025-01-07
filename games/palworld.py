
from games.rcon_game import RCONGame
from players import BasePlayer, SteamPlayer


class Palworld(RCONGame):
    PLAYER_TYPE = SteamPlayer

    def get_players(self) -> tuple[BasePlayer, ...]:
        """Get a list of players currently on the server."""
        players = Palworld._parse_list(self.send('ShowPlayers', enforce_id=False))
        self._log.debug(f"Players Online: {', '.join([p.name for p in players])}")
        return players

    @staticmethod
    def _parse_list(text: str) -> 'tuple[SteamPlayer, ...]':
        lines = text.splitlines()[1:]   # Toss header line.
        players = []
        for line in lines:
            if not line:
                continue
            name, uid, id = line.rsplit(',', maxsplit=2)
            players.append(SteamPlayer(name, int(uid), int(id)))
        return tuple(players)


if __name__ == "__main__":
    game = Palworld('localhost', 25575, "your_password")
    print(game.get_players())
