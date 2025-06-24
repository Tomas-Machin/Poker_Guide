import unittest
from Logic.Game import PokerGame

class TestPokerGameInitialization(unittest.TestCase):

    def setUp(self):
        self.user_position = "CO"
        self.num_players = 5
        self.blinds = 0.02
        self.user_hand = ["AS", "KD"]
        self.players_pockets = {
            "HJ": 50,
            "CO": 100,
            "BU": 75,
            "SB": 50,
            "BB": 30
        }

        self.game = PokerGame(
            self.user_position,
            self.num_players,
            self.blinds,
            self.user_hand,
            self.players_pockets
        )

    def test_deal_cards_and_assign_money(self):
        self.game.deal_cards_and_assign_money()
        poker_table = self.game.table.poker["Positions"]

        self.assertEqual(poker_table["CO"]["name"], "User")
        self.assertEqual(poker_table["CO"]["Chips"], 100)
        self.assertEqual(poker_table["CO"]["hand"], ["AS", "KD"])

        self.assertEqual(poker_table["HJ"]["Chips"], 50)
        self.assertEqual(poker_table["BU"]["Chips"], 75)

