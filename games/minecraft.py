
from games.rcon_game import RCONGame
from players import BasicPlayer


class Minecraft(RCONGame, player_type=BasicPlayer):

    def get_players(self) -> list[str]:
        # Get currently online players.
        # Example: 'There are 1 of a max of 20 players online: fossum99'
        raw = self.send('/list')
        player_str = raw.split(': ')[1]
        if player_str.strip() == '':
            players = []
        else:
            players = [BasicPlayer(p.strip()) for p in raw.split(': ')[1].split(',')]
        self._log.info(f"Players Online: {', '.join([p.name for p in players])}")
        return players


if __name__ == "__main__":
    rcon = Minecraft('192.168.1.65', 25576, "OurRCONP@ssword")
    print(rcon.get_players())
