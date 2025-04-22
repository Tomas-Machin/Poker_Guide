from Logic.Algorithms.Bayesian_Network import Network
from Objects.Table.Table import Table

GAME_ROUNDS = ["PREFLOP", "POSTFLOP", "TURN", "RIVER"]
FALLEN_POT = 0

def roundDecisions(num_players, blinds, user_position, players_pockets, user_hand, positions, actions, pot_in_bets):
    if GAME_ROUNDS[0] == 'PREFLOP':
        table_info = Table(num_players, blinds) # table_info.positions
        positions = table_info.positions
    print(f"\nRonda {GAME_ROUNDS[0]}.")   # ver como actualizar el valor de ROUND
    pot_in_bets, players_left, actions = playerAction(num_players, blinds, user_position, players_pockets, user_hand, positions, actions, pot_in_bets)
    roundResult(pot_in_bets, actions, players_left, blinds, user_position, players_pockets, user_hand, positions) 
    return sum(pot_in_bets)

def playerAction(num_players, blinds, user_position, players_pockets, user_hand, positions, actions, pot_in_bets):
    players_left = 0
    if GAME_ROUNDS[0] == "PREFLOP":
        pot_in_bets, actions = basePot_ActionsTable(num_players, blinds)

    for i in range(0, num_players):
        # print("Jugadores e indice: ", num_players, i)
        if (positions[i] == user_position):
            bynet = Network(user_position, players_pockets[user_position], blinds, user_hand, players_left)
            bynet.result_network()
        bet = input(f"Cantidad de apuesta (vacío - FOLD) de la posicion: {positions[i]}: ")
        
        actions, pot_in_bets, players_left = decisionResult(bet, actions, pot_in_bets, blinds, players_left, i, positions)
                
        print(pot_in_bets, ' | ', actions)

    players_left = num_players - players_left   # solo en la primera ronda -> puedo actualizar la variable num_players
    # print("Jugadores restantes: ", players_left)
    
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
        
def decisionResult(bet, actions, pot_in_bets, blinds, players_left, index, positions):
    previous_bets = pot_in_bets
    # FOLD
    if bet == '':
        actions[index] = "FOLD"
        players_left += 1
        print(f"Ha foldeado la posición: {positions[index]}.")
    else:
        if GAME_ROUNDS[0] == "PREFLOP":
            max_bet = max(pot_in_bets)
            # CALL 1º RONDA DE CIEGAS
            if float(bet) == blinds/2 and max(pot_in_bets) == blinds and positions[index] == 'SB' or float(bet) + blinds/2 == max_bet:
                pot_in_bets[index] += float(bet)
                actions[index] = "CALL"
                print(f"1-Ha calleado la posición: {positions[index]}.")
            elif float(bet) == 0 and max(pot_in_bets) == blinds and positions[index] == 'BB' or float(bet) + blinds == max_bet:
                pot_in_bets[index] += float(bet)
                actions[index] = "CALL"
                print(f"2-Ha calleado la posición: {positions[index]}.")
            # HACER RAISE
            elif float(bet) + pot_in_bets[index] > max_bet:
                max_bet = float(bet)
                pot_in_bets[index] += float(bet)
                actions[index] = "RAISE"
                print(f"1-Ha raiseado la posición: {positions[index]}.")
            # HACER CALL 
            elif float(bet) + pot_in_bets[index] == max_bet:
                pot_in_bets[index] += float(bet)
                actions[index] = "CALL"
                print(f"3-Ha calleado la posición: {positions[index]}.") 
            else:
                exit("La apuesta realizada no es valida.")      
                # dejar tomar la decision otra vez?    
        else:
            max_bet = 0
            print("Rondas posteriores: ", bet, previous_bets[index], pot_in_bets[index], index)
            # CHECK
            if bet == 0 and (previous_bets[index - 1] == pot_in_bets[index - 1] or index == 0):     # este if no funciona
                actions[index] = "CHECK"
                print(f"Ha chequeado la posición: {positions[index]}.")
            elif float(bet) + pot_in_bets[index] > max_bet and bet != 0:
                max_bet = float(bet)
                pot_in_bets[index] += float(bet)
                actions[index] = "RAISE"
                print(f"2-Ha raiseado la posición: {positions[index]}.")
            # HACER CALL 
            elif float(bet) + pot_in_bets[index] == max_bet:
                pot_in_bets[index] += float(bet)
                actions[index] = "CALL"
                print(f"4-Ha calleado la posición: {positions[index]}.") 
            else:
                exit("La apuesta realizada no es valida.")      
                # dejar tomar la decision otra vez?
        
    
    return actions, pot_in_bets, players_left

def roundResult(pot_in_bets, actions, players_left, blinds, user_position, players_pockets, user_hand, positions):
    result = ''
    if actions.count("CALL") == 1 and actions.count("FOLD") == len(actions) - 1:
        print(f"Ha ganado la posición {positions[actions.index("CALL")]}.")
    elif actions.count("RAISE") == 1 and actions.count("FOLD") == len(actions) - 1:
        print(f"Ha ganado la posición {positions[actions.index("RAISE")]}.")
    else:    
        print("\nSe vuelven a tomar decisiones.")
        for i in range(0, len(actions)):
            # print(i, pot_in_bets[i], max(pot_in_bets), actions[i], num_players)
            if pot_in_bets[i] < max(pot_in_bets) and actions[i] != "FOLD":  
                # FALTA LA RED BAYESIANA
                bet = input(f"Cantidad de apuesta (vacío - FOLD) de la posicion: {positions[i]}: ")
                actions, pot_in_bets, players_left = decisionResult(bet, actions, pot_in_bets, blinds, players_left, i, positions)
                print(pot_in_bets, ' | ', actions)
            if pot_in_bets.count(max(pot_in_bets)) == actions.count("RAISE") + actions.count("CALL"):
                result = 'Next Round'

        if result == 'Next Round':
            positions, actions, pot_in_bets = adjustTable(positions, actions, pot_in_bets)
            del GAME_ROUNDS[0]
            if len(GAME_ROUNDS) == 0:
                exit("La partida ha terminado.")
            roundDecisions(players_left, blinds, user_position, players_pockets, user_hand, positions, actions, pot_in_bets)
        else: 
            roundResult(pot_in_bets, actions, players_left, blinds, user_position, players_pockets, user_hand, positions)

def adjustTable(positions, actions, pot_in_bets):
    global FALLEN_POT
    i = 0

    while i < len(positions):
        if actions[i] == "FOLD":
            del positions[i]
            del actions[i]
            FALLEN_POT += pot_in_bets[i]
            del pot_in_bets[i]
        else:
            i += 1

    return positions, actions, pot_in_bets
        
