import unittest
from unittest.mock import patch
from Logic.Development import playerAction, roundDecisions, FALLEN_POT, GAME_ROUNDS
from Objects.Table.Table import Table

class TestPokerFlow(unittest.TestCase):

    def setUp(self):
        self.num_players = 3
        self.blinds = 0.2
        self.user_position = "BU"
        self.players_pockets = {"BU": 1000, "SB": 1000, "BB": 1000}
        self.user_hand = ["AS", "AC"]
        self.positions = ["BU", "SB", "BB"]
        self.actions = ["", "", ""]
        self.pot_in_bets = []
        self.round_bets = []
        self.table = Table(self.num_players, self.blinds)
        self.positions = self.table.positions

    @patch("builtins.input", side_effect=[
        "0.2",      # BU -> CALL
        "",         # SB -> FOLD
        "0",        # BB -> CHECK
        "QH 7D 10H", # cartas comunitarias POSTFLOP
        "0",        # BU -> CHECK (POSTFLOP)
        "0",        # BB -> CHECK (POSTFLOP)
        "9C",       # carta comunitaria TURN
        "0",        # BU -> CHECK (TURN)
        "0",        # BB -> CHECK (TURN)
        "8H",       # carta comunitaria RIVER
        "0",        # BU -> CHECK (RIVER)
        "0"         # BB -> CHECK (RIVER)
    ])
    def test_full_round_with_folds_and_checks(self, mock_input):

        roundDecisions(
            num_players=self.num_players,
            blinds=self.blinds,
            user_position=self.user_position,
            players_pockets=self.players_pockets,
            user_hand=self.user_hand,
            positions=self.positions,
            actions=self.actions,
            pot_in_bets=self.pot_in_bets,
            round_bets=self.round_bets
        )

        self.assertEqual(GAME_ROUNDS, [])

        expected_fallen_pot = self.blinds / 2
        self.assertEqual(FALLEN_POT, expected_fallen_pot)

        remaining_positions = ["BU", "BB"]
        self.assertListEqual(sorted(self.positions[:2]), sorted(remaining_positions))

