from Logic.Validations import Validations
#from Algorithms.Bayesian_Network import Network

POKER_POSITIONS = ["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]

def info_registration():
    try:
        user_position = input("Introduce tu posición en la mesa (UTG, MP, HJ, CO, BU, SB, BB): ").upper()
        num_players = int(input("Introduce el número de jugadores (2-7): "))
        blinds = float(input("Introduce las ciegas de la mesa (Mín. 0.02): "))
    except:
        exit('\nLos datos introducidos son inválidos.\n')

    user_hand = input("Introduce tu mano con el formato (7H 9C) siendo los palos H, S, C, D (Hearts, Spades, Cloves, Diamonds): ").upper().split()
    
    players_pockets = {"UTG": 0, "MP": 0, "HJ": 0, "CO": 0, "BU": 0, "SB": 0, "BB": 0}
    for i in range(0, num_players):
        money = input(f"Introduce las ciegas del jugador en la posicion: {POKER_POSITIONS[i]}: ")
        if money == '': money = 0 
        if float(money) > 0:
            players_pockets[POKER_POSITIONS[i]] = money

    validations = Validations(user_position, num_players, POKER_POSITIONS, blinds, user_hand, players_pockets)
    validations.confirm_data()

    return user_position, num_players, blinds, user_hand , players_pockets
