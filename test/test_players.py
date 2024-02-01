
from pathlib import Path
import unittest

from players import Player


class TestPlayer(unittest.TestCase):
    sample_data_path = Path(__file__).parent / 'showplayers_sample.txt'

    def setUp(self) -> None:
        self.sample_data = TestPlayer.sample_data_path.read_text()
        return super().setUp()

    def test_parse(self):
        act = Player.parse_list(self.sample_data)
        self.assertEqual(len(act), len(self.sample_data.splitlines()) - 1)
        self.assertIsInstance(act[0], Player)


if __name__ == "__main__":
    unittest.main()
