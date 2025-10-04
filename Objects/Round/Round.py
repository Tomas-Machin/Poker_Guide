class Round:
    def __init__(self, community_cards, blinds, playersInRound):
        self.ronda = {
            "Phase": "PREFLOP",
            "PlayersLeft": playersInRound,
            "Pot": "{0:.2f}".format(blinds + blinds / 2),
            "SidePot": [],
            "CommunityCards": community_cards
        }
