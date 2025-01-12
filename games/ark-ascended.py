from games.rcon_game import RCONGame
from players import SteamPlayer


class ArkAscended(RCONGame, player_type=SteamPlayer):

    @staticmethod
    def check_response(raw: str) -> None:
        errors = [
            "Server received, But no response!!"
        ]
        for error in errors:
            if error in raw:
                raise ValueError(error)

    def get_players(self) -> list[SteamPlayer]:
        # Get currently online players.
        # Example: "01. SteamID: 76561197960435530, Name: Haldor, Ping: 18
        # 02. SteamID: 76561198138884712, Name: Ljosalfar, Ping: 38"
        raw = self.send("ListPlayers")
        self.check_response(raw)
        if "No Players Connected" in raw:
            return []
        players = []
        for line in raw.splitlines():
            if not line.strip():
                continue  # Skip empty lines
            parts = line.split(',')
            steam_id_str = parts[0].split(':')[1].strip()
            name = parts[1].split(':')[1].strip()
            players.append(SteamPlayer(name, int(steam_id_str)))

        self._log.info(f"Players Online: {', '.join([p.name for p in players])}")
        return players


if __name__ == "__main__":
    rcon = ArkAscended('192.168.1.65', 27020, "hillside")
    print(rcon.get_players())
