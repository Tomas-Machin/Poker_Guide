import random
from .Deck import Deck

DECK = Deck()

class DeckMethods:
        def shuffle(self):
                random.shuffle(DECK.cards)

        def draw_card(self):
                return DECK.cards.pop()