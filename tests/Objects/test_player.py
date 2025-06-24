import unittest
from Objects.Player.Player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.valid_positions = ["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]
        self.position = "CO"
        self.hand = ['AS', 'KD']
        self.chips = 500
        self.player = Player(self.position, self.hand, self.chips)

    def test_player_position_is_valid(self):
        self.assertIn(self.player.position, self.valid_positions)

    def test_chips_greater_than_zero(self):
        self.assertGreater(self.player.chips, 0)

    def test_hand_has_two_cards(self):
        self.assertEqual(len(self.player.hand), 2)

    def test_hand_cards_are_different(self):
        self.assertNotEqual(self.player.hand[0], self.player.hand[1])

    def test_hand_cards_format(self):
        for card in self.player.hand:
            self.assertEqual(len(card), 2)
            self.assertIn(card[0], "23456789TJQKA")
            self.assertIn(card[1], "HSCD")

if __name__ == '__main__':
    unittest.main()
