import unittest
from unittest.mock import patch
import Logic.Development as dev
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
        "0.2",      
        "",         
        "0",        
        "QH 7D 10H", 
        "0",        
        "0",        
        "9C",       
        "0",        
        "0",        
        "8H",       
        "0",        
        "0"        
    ])
    def test_full_round_with_folds_and_checks(self, mock_input):
        
        dev.roundDecisions(
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

        self.assertEqual(dev.GAME_ROUNDS, [])

        expected_fallen_pot = self.blinds / 2
        self.assertEqual(dev.FALLEN_POT, expected_fallen_pot)

        remaining_positions = ["BB", "BU"]
        self.assertListEqual(dev.positions_arranged, remaining_positions)

