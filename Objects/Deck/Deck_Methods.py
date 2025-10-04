import random
from .Deck import Deck

DECK = Deck()

class DeckMethods:
        # ESTOS METODOS NO SE INVOLUCRAN EN NADA ACTUALMENTE
        def shuffle(self):
                random.shuffle(DECK.cards)

        def draw_card(self):
                return DECK.cards.pop()