import unittest
from Logic.Validations import Validations

class TestValidations(unittest.TestCase):

    def setUp(self):
        self.valid_data = {
            "num_players": 5,
            "user_position": "CO",
            "positions": ["HJ", "CO", "BU", "SB", "BB"],
            "blinds": 0.05,
            "hand": ["AS", "KD"],
            "players_pockets": {"CO": 1000}
        }

    def create_validator(self, override={}):
        data = self.valid_data.copy()
        data.update(override)
        return Validations(
            user_position=data["user_position"],
            num_players=data["num_players"],
            positions=data["positions"],
            blinds=data["blinds"],
            hand=data["hand"],
            players_pockets=data["players_pockets"]
        )

    def test_invalid_number_of_players(self):
        for n in [1, 8]:
            v = self.create_validator({"num_players": n})
            with self.assertRaises(ValueError) as e:
                v.validate_number_of_players()

    def test_invalid_user_position(self):
        v = self.create_validator({"user_position": "UTG"})
        with self.assertRaises(ValueError):
            v.validate_user_position()



if __name__ == '__main__':
    unittest.main()
