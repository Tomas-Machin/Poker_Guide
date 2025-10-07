from Logic.Validations import Validations
from Objects.Table.Table import Table
from Objects.Player.Player import Player

def info_registration():
    try:
        num_players = int(input("Introduce el número de jugadores (2-7): "))    
        blinds = float(input("Introduce las ciegas de la mesa (Mín. 0.02): "))
        table_info = Table(num_players, blinds)
        user_position = input(f"Introduce tu posición en la mesa {table_info.positions}: ").upper()
    except:
        exit('\nLos datos introducidos son inválidos.\n')

    user_hand = input("Introduce tu mano con el formato (7H 9C) siendo los palos H, S, C, D (Hearts, Spades, Cloves, Diamonds): ").upper().split()

    players_pockets = {"UTG": 0, "MP": 0, "HJ": 0, "CO": 0, "BU": 0, "SB": 0, "BB": 0}
    for i in range(0, num_players):
        money = input(f"Introduce las ciegas del jugador en la posicion: {table_info.positions[i]}: ")
        if money == '': money = 0 
        if float(money) > 0:
            players_pockets[table_info.positions[i]] = money

    return process_registration_data(num_players, blinds, user_position, user_hand, players_pockets)

def process_registration_data(num_players, blinds, user_position, user_hand, players_pockets):
    table_info = Table(num_players, blinds)
    user = Player(user_position, user_hand, players_pockets[user_position])
    validations = Validations(user_position, num_players, table_info.positions, blinds, user_hand, players_pockets)
    validations.confirm_data()

    return deal_cards_and_assign_money(table_info, user_position, players_pockets, user)
def deal_cards_and_assign_money(table_info_poker, user_position, players_pockets, user):
    table_info_poker.poker["Positions"][user_position]["name"] = "User"
    table_info_poker.poker["Positions"][user_position]["Chips"] = players_pockets[user_position]
    table_info_poker.poker["Positions"][user_position]["hand"] = user.hand
    for index, position in enumerate(table_info_poker.positions):
        if user_position == position:
            user.chips = players_pockets[position]
        else:
            table_info_poker.poker["Positions"][position]["Chips"] = players_pockets[position]

    print(user_position, table_info_poker.poker["TotalPlayers"], table_info_poker.poker["Blinds"], user.hand, players_pockets)

    return user_position, table_info_poker.poker["TotalPlayers"], table_info_poker.poker["Blinds"], user.hand, players_pockets

def game_information(self):

    print("\nInformación del juego inicialmente:")
    print(self.table.get_table_info())