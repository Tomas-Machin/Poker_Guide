class Validations:
    def __init__(self, num_players, user_position, positions, blinds, hand, chips):
        self.num_players = num_players
        self.user_position = user_position
        self.positions = positions
        self.blinds = blinds
        self.hand = hand
        self.chips = chips

    def validate_number_of_players(self, num_players):
        if num_players < 2 or num_players > 7:
            exit("\nLa cantidad de jugadores no es correcta.\n")

    def validate_user_position(self, user_position, positions):
        if user_position not in positions:
            exit("\nLa posición introducida es inválida o no esta en una mesa de ese tamaño.\n")

    def validate_blinds(self, blinds):
        if blinds < 0.02: # falla y ns porque - if isinstance(blinds, str) or float(blinds) < 0.02:
            exit("\nLas ciegas introducidas no son válidas.\n")

    def validate_user_hand(self, hand):
        if len(hand) != 2 or not (card in self.deck.cards for card in hand) or hand[0] == hand[1]:
            exit("\nLa mano introducida no son válidas.\n")

    # Hacer q pueda jugar sin las chips -> hacer q por defecto sean 0 *
    def validate_chips(self, chips):
        for player_chips in chips:
            if player_chips == '':      # *
                player_chips = 0
            if float(player_chips) <= 0:
                exit("\nLas fichas de algun jugador no son válidas.\n")

    def confirm_data(self):
        self.validate_user_position(self.user_position, self.positions)
        self.validate_number_of_players(self.num_players)
        self.validate_blinds(self.blinds)
        self.validate_user_hand(self.hand)
        self.validate_chips(self.chips)