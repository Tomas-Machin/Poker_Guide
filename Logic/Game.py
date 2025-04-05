from Objetcs.Deck import Deck
from Objetcs.Player import Player
#from Objetcs.Round import Round
from Objetcs.Table import Table
from Validations import Validations
"""from deck import Deck
from player import Player
from table import Table
from round import Round
from validations import Validations"""

class PokerGame:
    def __init__(self, num_players, user_position, blinds, user_hand, players_pockets):
        self.rivals = [Player("Rival", []) for _ in range(num_players - 1)]
        self.user_position = user_position
        self.table = Table(num_players, blinds)
        self.user = Player(user_position, user_hand, players_pockets[user_position])    
        # me renta usar un objeto Player o uso directament el de Mesa | si pq en el futuro es mejor para los rangos de cartas
        self.players_pockets = players_pockets
        self.deck = Deck()
        self.validations = Validations(num_players, user_position, self.table.positions, blinds, user_hand, players_pockets)
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

    """def deal_community_cards(self,):
        if(self.round.ronda['Round'] == 1):
            cards = [self.deck.draw_card() for _ in range(4)].pop(0)
            self.round = Round(self.round.pot, cards)"""

    def start_game(self):
        self.deck.shuffle()
        self.deal_cards_and_assign_money()
        self.validations.confirm_data()
        # self.play_rounds()

    def game_information(self):
        print("\nCartas del jugador usuario:")
        print(f"{self.user.name}: {self.user.hand}")

        #print("\nInformación del juego inicialmente:")
        #print(self.table.get_table_info())

        # print("\nPreflop round:")
        # print(self.round.ronda)

    """def play_rounds(self):
        # Aquí irán las rondas de apuestas y lógica adicional
        pass"""