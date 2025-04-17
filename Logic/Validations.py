from Objects.Deck.Deck import Deck

class Validations:
    def __init__(self, user_position, num_players, positions, blinds, hand, players_pockets):
        self.num_players = num_players
        self.user_position = user_position
        self.positions = positions
        self.blinds = blinds
        self.hand = hand
        self.players_pockets = players_pockets

    def validate_number_of_players(self):
        if self.num_players < 2 or self.num_players > 7:
            exit("\nLa cantidad de jugadores no es correcta.\n")

    def validate_user_position(self):
        if self.user_position not in self.positions:
            exit("\nLa posición introducida es inválida o no esta en una mesa de ese tamaño.\n")

    def validate_blinds(self):
        if self.blinds < 0.02: # falla y ns porque - if isinstance(blinds, str) or float(blinds) < 0.02:
            exit("\nLas ciegas introducidas no son válidas.\n")

    def validate_user_hand(self):
        deck = Deck()
        if not isinstance(self.hand, list) or len(self.hand) != 2:
            exit("La mano debe contener exactamente dos cartas.")

        card1 = self.hand[0].strip().upper()
        card2 = self.hand[1].strip().upper()

        if card1 not in deck.cards:
            exit(f"{card1} no es una carta válida.")
        if card2 not in deck.cards:
            exit(f"{card2} no es una carta válida.")
        if card1 == card2:
            exit("Las cartas no pueden ser iguales.")

    # Hacer q pueda jugar sin las chips -> hacer q por defecto sean 0 *
    def validate_chips(self):
        if float(self.players_pockets[self.user_position]) <= 0:
            exit("\nLas fichas de algun jugador no son válidas.\n")

# QUEDAN VALIDACIONES DE LAS APUESTAS E INPUTS DE CADA RONDA

# VER SI HACER UN ARCHIVO CON VARIABLES GLOBALES -> LO MAS OPTIMO SEGURAMENTE

    def confirm_data(self):
        self.validate_user_position()
        self.validate_number_of_players()
        self.validate_blinds()
        self.validate_user_hand()
        self.validate_chips()