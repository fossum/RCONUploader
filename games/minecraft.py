import gamedig

from games.base_game import Game
from players import BasicPlayer


class Minecraft(Game):
    PLAYER_TYPE = BasicPlayer

    def get_players(self) -> tuple[str]:
        """Get a list of players currently on the server.

        Returns:
            list[str]: A list of player names.
        """
        response = gamedig.query(game_id="minecraft", address=self._host, port=self._port)
        players = response["players"]
        if players is None:
            players = []
        return tuple(BasicPlayer(p["name"]) for p in players)


if __name__ == "__main__":
    rcon = Minecraft('192.168.1.65', 25565, "OurRCONP@ssword")
    print(rcon.get_players())
