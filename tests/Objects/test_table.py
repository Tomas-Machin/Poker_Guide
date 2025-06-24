import unittest
import json
from Objects.Table.Table import Table

class TestTable(unittest.TestCase):

    def setUp(self):
        self.num_players = 5
        self.blinds = 0.02
    
    def test_assign_positions_valid_num_players(self):
        expected_positions = {
            2: ["SB", "BB"],
            3: ["BU", "SB", "BB"],
            4: ["CO", "BU", "SB", "BB"],
            5: ["HJ", "CO", "BU", "SB", "BB"],
            6: ["MP", "HJ", "CO", "BU", "SB", "BB"],
            7: ["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]
        }

        for self.num_players, positions in expected_positions.items():
            table = Table(self.num_players, self.blinds)
            self.assertEqual(table.positions, positions)

    def test_table_data_assigned(self):
        table = Table(self.num_players, self.blinds)
        self.assertEqual(table.poker["Blinds"], self.blinds)
        self.assertEqual(table.poker["Players"], self.num_players)

    def test_table_positions_all_rival_initially(self): 
        table = Table(self.num_players, self.blinds)
        for pos, info in table.poker["Positions"].items():
            self.assertEqual(info, {"name": "Rival"})

    def test_get_table_info_returns_valid_json(self):
        table = Table(self.num_players, self.blinds)
        json_str = table.get_table_info()
        
        self.assertIsInstance(json_str, str)
        data = json.loads(json_str)

        self.assertEqual(data["Blinds"], self.blinds)
        self.assertEqual(data["Players"], self.num_players)
        self.assertEqual(set(data["Positions"].keys()), set(table.positions))

if __name__ == '__main__':
    unittest.main()
