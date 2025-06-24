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
        self.assertIn(self.player.position, self.valid_positions, "Posición no válida")



if __name__ == '__main__':
    unittest.main()
