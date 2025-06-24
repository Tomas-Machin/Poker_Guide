import unittest
import json
from Objects.Table.Table import Table

class TestTable(unittest.TestCase):

    def test_assign_positions_valid_num_players(self):
        expected_positions = {
            2: ["SB", "BB"],
            3: ["BU", "SB", "BB"],
            4: ["CO", "BU", "SB", "BB"],
            5: ["HJ", "CO", "BU", "SB", "BB"],
            6: ["MP", "HJ", "CO", "BU", "SB", "BB"],
            7: ["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]
        }
        num_players = 5
        for num_players, positions in expected_positions.items():
            table = Table(num_players, blinds=0.02)
            self.assertEqual(table.positions, positions)

    

if __name__ == '__main__':
    unittest.main()
