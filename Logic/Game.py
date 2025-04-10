from Objects.Deck import Deck
from Objects.Player import Player
#from Objetcs.Round import Round
from Objects.Table import Table

class PokerGame:
    def __init__(self, user_position, num_players, blinds, user_hand, players_pockets):
        self.rivals = [Player("Rival", []) for _ in range(num_players - 1)]
        self.user_position = user_position
        self.table = Table(num_players, blinds)
        self.user = Player(user_position, user_hand, players_pockets[user_position])    
        # me renta usar un objeto Player o uso directament el de Mesa | si pq en el futuro es mejor para los rangos de cartas
        self.players_pockets = players_pockets
        self.deck = Deck()
        self.assign_user_into_positions()

    def assign_user_into_positions(self):
        for position in self.table.positions:
            if self.user_position == position:
                self.table.poker["Positions"][self.user_position]["name"] = self.user.name

    def deal_cards_and_assign_money(self):
        for index, position in enumerate(self.table.positions):
            if self.user_position == position:
                self.table.poker["Positions"][self.user_position]["Chips"] = self.players_pockets[index]
                self.user.chips = self.players_pockets[index]
                self.table.poker["Positions"][self.user_position]["hand"] = self.user.hand
            else:
                self.table.poker["Positions"][position]["Chips"] = self.players_pockets[index]
                #self.table.poker["Positions"][position]["hand"] = [self.deck.draw_card() for _ in range(2)]

    def start_game(self):
        self.deck.shuffle()
        self.deal_cards_and_assign_money()

    def game_information(self):
        print("\nCartas del jugador usuario:")
        print(f"{self.user.name}: {self.user.hand}")

        #print("\nInformación del juego inicialmente:")
        #print(self.table.get_table_info())

        # print("\nPreflop round:")
        # print(self.round.ronda)