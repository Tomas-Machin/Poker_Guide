POKER_POSITIONS = ["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]       # usar las posiciones de la mesa (Table) en vez de esto
REARRANGE_POSITIONS = ["SB", "BB", "UTG", "MP", "HJ", "CO", "BU"]
GAME_ROUNDS = ["PREFLOP", "POSTFLOP", "TURN", "RIVER"]
ROUND = 0

from Logic.Algorithms.Bayesian_Network import Network

def roundDecisions(num_players, blinds, user_position, players_pockets, user_hand):
    print(f"Ronda {GAME_ROUNDS[0]}.")   # ver como actualizar el valor de ROUND
    pot_in_bets, players_left, actions = playerAction(num_players, blinds, user_position, players_pockets, user_hand)
    roundResult(pot_in_bets, actions, players_left, blinds, user_position, players_pockets, user_hand) 
    return sum(pot_in_bets)

# def firstRoundDecisions(num_players, blinds, user_position, players_pockets, user_hand):
#     print(f"Ronda {GAME_ROUNDS[0]}.")
#     pot_in_bets, players_left, actions = playerAction(num_players, blinds, user_position, players_pockets, user_hand)
#     roundResult(pot_in_bets, actions, players_left, blinds) 
#     return sum(pot_in_bets)

# def nextRoundsDecisions(players_left, pot_in_bets, actions, blinds, user_position, players_pockets, user_hand):
#     pot_in_bets, players_left, actions = playerAction(players_left, blinds, user_position, players_pockets, user_hand)
#     roundResult(pot_in_bets, actions, players_left, blinds) 
#     return sum(pot_in_bets)

def playerAction(num_players, blinds, user_position, players_pockets, user_hand):
    players_left = POKER_POSITIONS
    if GAME_ROUNDS[0] == "PREFLOP":
        pot_in_bets, actions = basePot_ActionsTable(num_players, blinds)
        del GAME_ROUNDS[0]

    for i in range(0, num_players):
        if (POKER_POSITIONS[i] == user_position):
            bynet = Network(user_position, players_pockets[user_position], blinds, user_hand, len(players_left))
            bynet.result_network()
        bet = input(f"Cantidad de apuesta (vacío - FOLD) de la posicion: {POKER_POSITIONS[i]}: ")
        
        actions, pot_in_bets, players_left = decisionResult(bet, actions, pot_in_bets, blinds, players_left, i)
                
        print(pot_in_bets, ' | ', actions)

    players_left = num_players - players_left   # solo en la primera ronda? -> puedo actualizar la variable num_players
    print(players_left)
    
    return pot_in_bets, players_left, actions

def basePot_ActionsTable(num_players, blinds):
    pot_in_bets = []
    actions = []
    for i in range(0, num_players):
        if i < num_players - 2:
            pot_in_bets.append(0)
            actions.append('')
        elif i == num_players - 2 :            
            pot_in_bets.append(blinds/2)
            actions.append('')
        else:
            pot_in_bets.append(blinds)
            actions.append('')

    return pot_in_bets, actions
        
def decisionResult(bet, actions, pot_in_bets, blinds, players_left, i):
    max_bet = max(pot_in_bets)
    # print(max_bet)
    # FOLD
    if bet == '':
        actions[i] = "FOLD"
        players_left += 1
        print(f"Ha foldeado la posición: {POKER_POSITIONS[i]}.")
    # CALL 1º RONDA DE CIEGAS
    elif float(bet) == blinds/2 and max(pot_in_bets) == blinds and POKER_POSITIONS[i] == 'SB' or float(bet) + blinds/2 == max_bet:
        pot_in_bets[i] += float(bet)
        actions[i] = "CALL"
        print(f"Ha calleado la posición: {POKER_POSITIONS[i]}.")
    elif float(bet) == 0 and max(pot_in_bets) == blinds and POKER_POSITIONS[i] == 'BB' or float(bet) + blinds == max_bet:
        pot_in_bets[i] += float(bet)
        actions[i] = "CALL"
        print(f"Ha calleado la posición: {POKER_POSITIONS[i]}.")
    # CALL RESTO DE JUGADORES SIN RAISE PREVIO
    elif float(bet) == max_bet:
        pot_in_bets[i] += float(bet)
        actions[i] = "CALL"
        print(f"Ha calleado la posición: {POKER_POSITIONS[i]}.") 
    # HACER RAISE
    elif float(bet) > max_bet:
        max_bet = float(bet)
        pot_in_bets[i] += float(bet)
        actions[i] = "RAISE"
        print(f"Ha raiseado la posición: {POKER_POSITIONS[i]}.")
    # HACER CALL AL RAISE
    elif float(bet) + pot_in_bets[i] == max_bet:
        pot_in_bets[i] += float(bet)
        actions[i] = "CALL"
        print(f"Ha calleado la posición: {POKER_POSITIONS[i]}.") 
    # HACER RAISE AL RAISE
    elif float(bet) + pot_in_bets[i] > max_bet:
        max_bet = float(bet)
        pot_in_bets[i] += float(bet)
        actions[i] = "RAISE"
        print(f"Ha raiseado la posición: {POKER_POSITIONS[i]}.")
    else:
        exit("La apuesta realizada no es valida.")      
        # dejar tomar la decision otra vez?    
    
    return actions, pot_in_bets, players_left

def roundResult(pot_in_bets, actions, players_left, blinds, user_position, players_pockets, user_hand):
    result = ''
    if actions.count("CALL") == 1 and actions.count("FOLD") == len(actions) - 1:
        print(f"Ha ganado la posición {POKER_POSITIONS[actions.index("CALL")]}.")
    elif actions.count("RAISE") == 1 and actions.count("FOLD") == len(actions) - 1:
        print(f"Ha ganado la posición {POKER_POSITIONS[actions.index("RAISE")]}.")
    else:    
        print("Se vuelven a tomar decisiones.")
        for i in range(0, len(actions)):
            # print(i, pot_in_bets[i], max(pot_in_bets), actions[i], num_players)
            if pot_in_bets[i] < max(pot_in_bets) and actions[i] != "FOLD":  # falta la red bayesiana
                bet = input(f"Cantidad de apuesta (vacío - FOLD) de la posicion: {POKER_POSITIONS[i]}: ")
                actions, pot_in_bets, players_left = decisionResult(bet, actions, pot_in_bets, blinds, players_left, i)
                print(pot_in_bets, ' | ', actions)
            if pot_in_bets.count(max(pot_in_bets)) == actions.count("RAISE") + actions.count("CALL"):
                result = 'Next Round'

        if result == 'Next Round':
            # print(f"Ronda {GAME_ROUNDS[ROUND]}.")
            roundDecisions(players_left, blinds, user_position, players_pockets, user_hand)
            # nextRoundsDecisions(players_left, pot_in_bets, actions, blinds, user_position, players_pockets, user_hand)
        else: 
            roundResult(pot_in_bets, actions, players_left, blinds, user_position, players_pockets, user_hand)

    # if roundResult() == NEXT -> se peude pasar de ronda