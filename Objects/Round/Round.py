class Round:
    def __init__(self, pot, community_cards, blinds, playersInRound):
        self.pot = "{0:.2f}".format(sum(pot) + blinds + blinds / 2)

        self.ronda = {
            "Fase": "PREFLOP",
            "PlayersLeft": playersInRound,
            "Pot": self.pot,
            "SidePot": [],
            "CommunityCards": community_cards
        }
