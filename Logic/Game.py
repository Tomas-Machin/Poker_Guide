#from Objects.Deck.Deck import Deck
from Objects.Deck.Deck_Methods import DeckMethods
from Objects.Player.Player import Player
#from Objetcs.Round import Round
from Objects.Table.Table import Table

class PokerGame:
    def __init__(self, user_position, num_players, blinds, user_hand, players_pockets):
        #self.rivals = [Player("Rival", [], __) for _, __ in players_pockets.items()]   # -> util pero en un NIVEL mayor
        self.user_position = user_position
        self.table = Table(num_players, blinds)
        self.user = Player(user_position, user_hand, players_pockets[user_position])    
        # me renta usar un objeto Player o uso directament el de Mesa | si pq en el futuro es mejor para los rangos de cartas
        self.players_pockets = players_pockets
        self.deck = DeckMethods()

    def deal_cards_and_assign_money(self):
        self.table.poker["Positions"][self.user_position]["name"] = "User"
        self.table.poker["Positions"][self.user_position]["Chips"] = self.players_pockets[self.user_position]
        self.table.poker["Positions"][self.user_position]["hand"] = self.user.hand
        for index, position in enumerate(self.table.positions):
            if self.user_position == position:
                self.user.chips = self.players_pockets[position]
            else:
                self.table.poker["Positions"][position]["Chips"] = self.players_pockets[position]

    def start_game(self):
        self.deck.shuffle()
        self.deal_cards_and_assign_money()

    def game_information(self):
        print("\nCartas del jugador usuario:")
        print(f"{self.user.name}: {self.user.position} - {self.user.hand}")

        print("\nInformación del juego inicialmente:")
        print(self.table.get_table_info())

        # print("\nPreflop round:")
        # print(self.round.ronda)