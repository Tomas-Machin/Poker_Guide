import random
from Deck import Deck

def shuffle(self):
        random.shuffle(Deck.cards)

def draw_card(self):
    return Deck.cards.pop()