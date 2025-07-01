class Round:
    def __init__(self, pot, community_cards, blinds, playersInRound):
        self.pot = "{0:.2f}".format(sum(pot) + blinds + blinds / 2)

        self.ronda = {
            "Round": 1,
            "Players left": playersInRound,
            "Pot": self.pot,
            "Community cards": community_cards
        }
