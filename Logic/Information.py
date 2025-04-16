from Logic.Validations import Validations
#from Algorithms.Bayesian_Network import Network

POKER_POSITIONS = ["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]
# POSITIONS_LEFT = ["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]    # creo q puedo hacerlo con POKER_POSITIONS

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

def firstDecision(num_players, blinds):   # de UTG a BB
    """
        - Restar dinero de los jugadores 
            - actualizar dinero de jugadores
            - actualizar dinero del pot
        - Quitar jugadores que hacen fold -> HECHO?
        - En caso de raise dar otra vuelta --> LO MAS COMPLICADO -> HECHO?
    """
    pot_in_bets, players_left, actions = playerAction(num_players, blinds)

    # for i in pot_in_bets:
    for i in range(0, num_players):
        print(i, actions[i], pot_in_bets[i])
        if(pot_in_bets[i] < max(pot_in_bets) and actions[i] != "FOLD" and actions[num_players - 1] != "FOLD"):    # jugador call - otro raise - fold no funciona
            print('Sigue la misma ronda.')
            pot_in_bets, players_left = playerAction(players_left, blinds)
        #elif(pot_in_bets.count(max(pot_in_bets)) == 1):
        else:
            # victoria
            exit(f"Ha ganado el bote la posicion: {POKER_POSITIONS[pot_in_bets.index(max(pot_in_bets))]}")

    # while (num_players > 1):
    #     playerAction(num_players, blinds)


    # for i in range(0, num_players):     # cambiar a un while
    #     if(user_position == POKER_POSITIONS[i]):
    #         bynet = Network(user_position, user_chips, blinds, user_hand, players_left)
    #         bynet.result_network()
    #         bet = float(input(f"Introduce tu apuesta: "))
    #         if bet == 0: break
    #     else:    
    #         bet = float(input(f"Cantidad de apuesta o FOLD (si precede) de la posicion: {POKER_POSITIONS[i]}: "))   # CALL es 
    #         # cambiar
    #         if bet == 'FOLD' and POKER_POSITIONS[i] != 'BB': # or bet == ''
    #             players_left += 1  # reducir el numero de jugadores
    #             print("Players left in the table: ", num_players - players_left)

    #     pot_in_bets.append(bet)
        # pot_in_bets[i] = bet

    return pot_in_bets, players_left

# Resto de decisiones de SB a BU

def playerAction(num_players, blinds):
    pot_in_bets = []
    actions = []
    players_left = 0

    for i in range(0, num_players):
        if(i < num_players - 2):
            pot_in_bets.append(0)
        elif(i == num_players - 2):            
            pot_in_bets.append(blinds/2)
        else:
            pot_in_bets.append(blinds)

        bet = input(f"Cantidad de apuesta (vacío - FOLD) de la posicion: {POKER_POSITIONS[i]}: ")

        if bet == '':
                actions.append("FOLD")
                players_left += 1
                print(f"Ha foldeado la posición: {POKER_POSITIONS[i]}.")
        elif float(bet) == 0 and POKER_POSITIONS[i] == 'BB':
                actions.append("CALL")
                print(f"Ha calleado la posición: {POKER_POSITIONS[i]}.")
        elif float(bet) == blinds:
            pot_in_bets[i] += float(bet)
            actions.append("CALL")
            print(f"Ha calleado la posición: {POKER_POSITIONS[i]}.") 
        elif float(bet) > blinds:
            pot_in_bets[i] += float(bet)
            actions.append("RAISE")
            print(f"Ha raiseado la posición: {POKER_POSITIONS[i]}.")
        else:
            exit("La apuesta realizada no es valida.")      
            # dejar tomar la decision otra vez?       
        
        print(pot_in_bets, ' | ', actions)
    
    return pot_in_bets, players_left, actions