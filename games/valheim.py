
from games.gd_game import GDGame
from players import BasicPlayer


class Valheim(GDGame, game_name="valheim"):
    PLAYER_TYPE = BasicPlayer

    def get_players(self) -> tuple[str]:
        """Get a list of players currently on the server.

        Returns:
            list[str]: A list of player names.
        """
        response = self.query()
        players = response["players"]
        if players is None:
            players = []
        return tuple(BasicPlayer(p["name"]) for p in players)


if __name__ == "__main__":
    game = Valheim('192.168.1.65')
    print(game.get_players())
