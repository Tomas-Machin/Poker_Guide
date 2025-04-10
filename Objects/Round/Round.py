class Round:
    def __init__(self, pot, community_cards, blinds, playersInRound):
        self.pot = "{0:.2f}".format(sum(pot) + blinds + blinds / 2)

        self.ronda = {
            "Round": 1,
            "Players left": playersInRound,
            "Pot": self.pot,
            "Community cards": community_cards
        }

        #objeto variable o hacer un objeto por ronda
        """self.ronda_1 = {
            "Players left": 1,  # PREFLOP
            "Pot": self.pot,
        }

        self.ronda_2 = {
            "Players left": 2,  # POSTFLOP
            "Pot": self.pot,
            "Community cards": self.community_cards
        }

        self.ronda_3 = {
            "Players left": 3,  # TURN
            "Pot": self.pot,
            "Community cards": self.community_cards
        }

        self.ronda_4 = {
            "Players left": 4,  # RIVER
            "Pot": self.pot,
            "Community cards": self.community_cards
        }"""