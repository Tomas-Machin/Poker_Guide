POKER_POSITIONS = ["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]
REARRANGE_POSITIONS = ["SB", "BB", "UTG", "MP", "HJ", "CO", "BU"]
GAME_ROUNDS = ["PREFLOP", "POSTFLOP", "TURN", "RIVER"]

from Information import info_registration
USER_POSITION, NUM_PLAYERS, BLINDS, USER_HAND, PLAYERS_POCKETS = info_registration()

def firstRoundDecisions(num_players, blinds, user_position):
    print(f"Ronda {GAME_ROUNDS[0]}.")
    pot_in_bets, players_left, actions = playerAction(num_players, blinds, user_position)
    roundResult(pot_in_bets, actions, players_left, blinds) 
    return sum(pot_in_bets)

def nextRoundsDecisions(players_left, pot_in_bets, actions, blinds):
    pot_in_bets, players_left, actions = playerAction(players_left, blinds)
    roundResult(pot_in_bets, actions, players_left, blinds) 
    return sum(pot_in_bets)

def playerAction(num_players, blinds, user_position):
    players_left = 0
    if GAME_ROUNDS[0] == "PREFLOP":
        pot_in_bets, actions = basePot_ActionsTable(num_players, blinds)

    for i in range(0, num_players):
        if (POKER_POSITIONS[i] == user_position):
            bynet = Network(user_position, user_chips, blinds, user_hand, players_left)
            bynet.result_network()
        bet = input(f"Cantidad de apuesta (vacío - FOLD) de la posicion: {POKER_POSITIONS[i]}: ")
        
        actions, pot_in_bets, players_left = decisionResult(bet, actions, pot_in_bets, blinds, players_left, i)
                
        print(pot_in_bets, ' | ', actions)

    players_left = num_players - players_left   # solo en la primera ronda -> puedo actualizar la variable num_players
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
    print(max_bet)
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

def roundResult(pot_in_bets, actions, players_left, blinds):
    result = ''
    if actions.count("CALL") == 1 and actions.count("FOLD") == len(actions) - 1:
        print(f"Ha ganado la posición {POKER_POSITIONS[actions.index("CALL")]}.")
    elif actions.count("RAISE") == 1 and actions.count("FOLD") == len(actions) - 1:
        print(f"Ha ganado la posición {POKER_POSITIONS[actions.index("RAISE")]}.")
    else:    
        print("Se vuelven a tomar decisiones.")
        for i in range(0, len(actions)):
            # print(i, pot_in_bets[i], max(pot_in_bets), actions[i], num_players)
            if pot_in_bets[i] < max(pot_in_bets) and actions[i] != "FOLD":
                # if POKER_POSITIONS[i] == "SB" and ROUND == "PREFLOP":
                #     continue
                bet = input(f"Cantidad de apuesta (vacío - FOLD) de la posicion: {POKER_POSITIONS[i]}: ")
                actions, pot_in_bets, players_left = decisionResult(bet, actions, pot_in_bets, blinds, players_left, i)
                print(pot_in_bets, ' | ', actions)
            if pot_in_bets.count(max(pot_in_bets)) == actions.count("RAISE") + actions.count("CALL"):
                result = 'Next Round'
                # nextRound(pot_in_bets, players_left)

        if result == 'Next Round':
            print(f"Ronda {GAME_ROUNDS[1]}.")
            #nextRoundsDecisions(players_left, pot_in_bets, actions, blinds)
        else: 
            roundResult(pot_in_bets, actions, players_left, blinds)

    # if roundResult() == NEXT -> se peude pasar de ronda