import unittest
from Logic.Development import basePot_ActionsTable, no_call_before_raise

class TestGameDevelopment(unittest.TestCase):

    def test_base_pot_actions_table_5_players(self):
        num_players = 5
        blinds = 2
        pot, round_bets, actions = basePot_ActionsTable(num_players, blinds)

        self.assertEqual(pot, [0, 0, 0, 1.0, 2.0])
        self.assertEqual(round_bets, [0, 0, 0, 0, 0])
        self.assertEqual(actions, ['', '', '', '', ''])

    def test_call_then_raise(self):
        actions = ['CALL', 'RAISE']
        self.assertTrue(no_call_before_raise(actions))

    def test_raise_then_call(self):
        actions = ['RAISE', 'CALL']
        self.assertTrue(no_call_before_raise(actions))

    def test_multiple_raises(self):
        actions = ['FOLD', 'RAISE', 'RAISE']
        self.assertTrue(no_call_before_raise(actions))

if __name__ == '__main__':
    unittest.main()

