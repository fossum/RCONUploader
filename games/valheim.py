
from games.gd_game import GDGame
from players import BasicPlayer


class Valheim(GDGame, game_name="valheim"):
    PLAYER_TYPE = BasicPlayer
    DEFAULT_PORT = 2457

    def get_players(self) -> tuple[BasicPlayer, ...]:
        """Get a list of players currently on the server.

        Returns:
            tuple[BasicPlayer, ...]: A list of online player names.
        """
        response = self.query()
        players = response["players"]
        if players is None:
            players = []
        return tuple(BasicPlayer(p["name"]) for p in players)


if __name__ == "__main__":
    game = Valheim('localhost')
    print(game.get_players())
