import unittest
from unittest.mock import patch
from Logic.Development import playerAction

class TestPokerGameFlow(unittest.TestCase):
    def setUp(self):
        self.num_players = 3
        self.blinds = 0.2
        self.user_position = "BU"
        self.players_pockets = {"BU": 1000, "SB": 1000, "BB": 1000}
        self.user_hand = ["AS", "AC"]
        self.positions = ["BU", "SB", "BB"]
        self.actions = ["", "", ""]
        self.pot_in_bets = [0, 0, 0]
        self.round_bets = [0, 0, 0]

    @patch("builtins.input", side_effect=["0.2", "", "0"])
    def test_3_player_preflop_call_fold_check(self, mock_input):
        pot_in_bets, players_left, actions, round_bets = playerAction(
            self.num_players,
            self.blinds,
            self.user_position,
            self.players_pockets,
            self.user_hand,
            self.positions,
            self.actions,
            self.pot_in_bets,
            self.round_bets
        )

        self.assertEqual(actions, ["CALL", "FOLD", "CHECK"])
        self.assertEqual(players_left, 2)
        self.assertEqual(pot_in_bets, [0.2, 0.1, 0.2])
