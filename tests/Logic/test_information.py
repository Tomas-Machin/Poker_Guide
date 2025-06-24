import unittest
from Logic.Information import process_registration_data

class TestInformationProcessing(unittest.TestCase):

    def setUp(self):
        self.valid_input = {
            "num_players": 5,
            "blinds": 0.02,
            "user_position": "CO",
            "user_hand": ["AS", "KD"],
            "players_pockets": {
                "HJ": 50, "CO": 100, "BU": 75, "SB": 50, "BB": 30
            }
        }

    def test_invalid_number_of_players(self):
        data = self.valid_input.copy()
        data["num_players"] = 1
        with self.assertRaises(ValueError):
            process_registration_data(**data)

    def test_invalid_blinds(self):
        data = self.valid_input.copy()
        data["blinds"] = 0.01
        with self.assertRaises(ValueError):
            process_registration_data(**data)

    def test_invalid_position(self):
        data = self.valid_input.copy()
        data["user_position"] = "BTN"
        with self.assertRaises(ValueError):
            process_registration_data(**data)

    def test_invalid_hand(self):
        data = self.valid_input.copy()
        data["user_hand"] = ["AS", "AS"]
        with self.assertRaises(ValueError):
            process_registration_data(**data)

    def test_invalid_chips(self):
        data = self.valid_input.copy()
        data["players_pockets"]["CO"] = 0
        with self.assertRaises(ValueError):
            process_registration_data(**data)

    def test_valid_data_returns_expected_data(self):
        result = process_registration_data(**self.valid_input)
        self.assertEqual(result[0], "CO")
        self.assertEqual(result[1], 5)
        self.assertEqual(result[2], 0.02)
        self.assertEqual(result[3], ["AS", "KD"])
        self.assertEqual(result[4],{"HJ": 50, "CO": 100, "BU": 75, "SB": 50, "BB": 30})

if __name__ == "__main__":
    unittest.main()

