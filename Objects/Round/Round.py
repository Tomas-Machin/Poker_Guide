class Round:
    def __init__(self, community_cards, blinds, playersInRound):
        self.pot = "{0:.2f}".format(blinds + blinds / 2)

        self.ronda = {
            "Fase": "PREFLOP",
            "PlayersLeft": playersInRound,
            "Pot": self.pot,
            "SidePot": [],
            "CommunityCards": community_cards
        }
