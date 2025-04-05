from Validations import Validations

Poker_positions = ["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]

def info_registration():
    #user_name = input("Introduce tu nombre: ")

    try:
        user_position = input("Introduce tu posición en la mesa (UTG, MP, HJ, CO, BU, SB, BB): ").upper()
        num_players = int(input("Introduce el número de jugadores (2-7): "))
        blinds = float(input("Introduce las ciegas de la mesa (Mín. 0.02): "))
    except:
        exit('\nLos datos introducidos son inválidos.\n')

    user_hand = input("Introduce tu mano con el formato (7H 9C) siendo los palos H, S, C, D (Hearts, Spades, Cloves, Diamonds): ").upper().split()

    # players_pockets = []    # usar un diccionario
    # for i in range(0, num_players):
    #     money = input(f"Introduce las ciegas del jugador en la posicion: {Poker_positions[i]}: ")
    #     players_pockets.append(money)
    
    players_pockets = {"UTG": 0, "MP": 0, "HJ": 0, "CO": 0, "BU": 0, "SB": 0, "BB": 0}
    for i in range(0, num_players):
        money = input(f"Introduce las ciegas del jugador en la posicion: {Poker_positions[i]}: ")
        players_pockets[Poker_positions[i]] = money

    validations = Validations()
    validations.confirm_data()

    return user_position, num_players, blinds, user_hand , players_pockets
