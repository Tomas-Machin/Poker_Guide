class Deck:
    def __init__(self):
        self.rank = "23456789TJQKA"
        self.suit = "HSCD"   # "♠♥♦♣"
        self.cards = [f"{rank}{suit}" for rank in self.rank for suit in self.suit]