import unittest
from Objects.Deck.Deck import Deck
from Objects.Deck.Deck_Methods import DeckMethods, DECK

class TestDeck(unittest.TestCase):

    def setUp(self):
        # Esto se ejecuta antes de cada test para resetear el mazo
        DECK.cards = [f"{rank}{suit}" for rank in "23456789TJQKA" for suit in "HSCD"]

    def test_deck_initialization(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)
        self.assertEqual(deck.cards[0], "2H")
        self.assertEqual(deck.cards[-1], "AD")

if __name__ == '__main__':
    unittest.main()

# py -m unittest tests/test_deck.py