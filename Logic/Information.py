from Logic.Validations import Validations
from Algorithms.Bayesian_Network import Network

POKER_POSITIONS = ["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]

def info_registration():
    #user_name = input("Introduce tu nombre: ")

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

def firstDecision(user_position, num_players, user_chips, blinds, user_hand):   # de UTG a BB
    """
        - Restar dinero de los jugadores 
            - actualizar dinero de jugadores
            - actualizar dinero del pot
        - Quitar jugadores que hacen fold
        - En caso de raise dar otra vuelta --> LO MAS COMPLICADO
    """
    pot_in_bets = []
    players_left = 0
    for i in range(0, num_players):
        if(user_position == POKER_POSITIONS[i]):
            bynet = Network(user_position, user_chips, blinds, user_hand, players_left)
            bynet.result_network()
            bet = float(input(f"Introduce tu apuesta: "))
            if bet == 0: break
        else:    
            bet = float(input(f"Cantidad de apuesta o FOLD (si precede) de la posicion: {POKER_POSITIONS[i]}: "))   # CALL es 0
            if bet == 0 and POKER_POSITIONS[i] != 'BB': # or bet == ''
                players_left += 1  # reducir el numero de jugadores
                print("Players left in the table: ", num_players - players_left)

        pot_in_bets.append(bet)

    return pot_in_bets, players_left

# Resto de decisiones de SB a BU