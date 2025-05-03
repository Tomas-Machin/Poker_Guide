from Logic.Algorithms.Bayesian_Network import Network
from Objects.Table.Table import Table

GAME_ROUNDS = ["PREFLOP", "POSTFLOP", "TURN", "RIVER"]
FALLEN_POT = 0
positions_arranged = []
actions_arranged = []
pot_in_bets_arranged = []

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
        bet = input(f"\nCantidad de apuesta (vacío - FOLD) de la posicion: {positions[i]}: ")
        
        actions, pot_in_bets, players_left = decisionResult(bet, actions, pot_in_bets, blinds, players_left, i, positions)
                
        print(pot_in_bets, ' | ', actions, ' | ', positions)

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
            if float(bet) == blinds/2 and max(pot_in_bets) == blinds and positions[index] == 'SB': # or float(bet) + blinds/2 == max_bet:
                pot_in_bets[index] = round(pot_in_bets[index] + float(bet), 2)
                actions[index] = "CALL"
                print(f"Ha calleado la posición: {positions[index]}.")
            elif float(bet) == 0 and max(pot_in_bets) == blinds and positions[index] == 'BB': # or float(bet) + blinds == max_bet:
                pot_in_bets[index] = round(pot_in_bets[index] + float(bet), 2)
                actions[index] = "CHECK"
                print(f"Ha chequeado la posición: {positions[index]}.")
            # HACER RAISE
            elif round(float(bet) + pot_in_bets[index], 2) > max_bet:
                max_bet = float(bet)
                pot_in_bets[index] = round(pot_in_bets[index] + float(bet), 2)
                actions[index] = "RAISE"
                print(f"Ha raiseado la posición: {positions[index]}.")
            # HACER CALL 
            elif round(float(bet) + pot_in_bets[index], 2) == max_bet:
                pot_in_bets[index] = round(pot_in_bets[index] + float(bet), 2)
                actions[index] = "CALL"
                print(f"Ha calleado la posición: {positions[index]}.") 
            else:
                exit("La apuesta realizada no es valida.")      
                # dejar tomar la decision otra vez?    
        else:   
            # PULIR MUCHO Y VER BIEN Q ES LO Q PASA
            max_bet = 0
            print("Estado ronda: ", bet, max_bet, previous_bets[index], pot_in_bets[index], index)
            # CHECK
            # if bet == max_bet and previous_bets[index] == pot_in_bets[index]:     # NO ENTRA
            if (index == 0 and float(bet) == max_bet) or (float(bet) == max_bet and previous_bets[index] == pot_in_bets[index]):
                actions[index] = "CHECK"
                print(f"Ha chequeado la posición: {positions[index]}.")
            # HACER RAISE
            elif float(bet) + pot_in_bets[index] > max_bet and bet != 0:    # ENTRA EL CHECK AQUI
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
    # TODOS FOLDS
    if actions.count("FOLD") == len(positions):
        exit("La partida ha terminado sin ganador.")
    # UN CALL Y RESTO FOLD
    elif actions.count("CALL") == 1 and actions.count("FOLD") == len(actions) - 1:
        print(f"Ha ganado la posición {positions[actions.index("CALL")]}.")
    # UN RAISE Y RESTO FOLD
    elif actions.count("RAISE") == 1 and actions.count("FOLD") == len(actions) - 1:
        print(f"Ha ganado la posición {positions[actions.index("RAISE")]}.")
    # DOS CALL O MAS SIN OTRA VUELTA DE DECISIONES
    elif no_call_before_raise(actions) == False:
        result = 'Next Round'
    # OTRA VUELTA DE DECISIONES EN CASO DE RAISE POSTERIOR
    else:    
        print("\nSe vuelven a tomar decisiones.")
        for i in range(0, len(actions)):
            # print(i, pot_in_bets[i], max(pot_in_bets), actions[i], num_players)
            if pot_in_bets[i] < max(pot_in_bets) and actions[i] != "FOLD":  # EDITAR CONDICION A TODOS RAISE
                if (positions[i] == user_position):
                    bynet = Network(user_position, players_pockets[user_position], blinds, user_hand, players_left)
                    bynet.result_network()
                bet = input(f"\nCantidad de apuesta (vacío - FOLD) de la posicion: {positions[i]}: ")
                actions, pot_in_bets, players_left = decisionResult(bet, actions, pot_in_bets, blinds, players_left, i, positions)
                print(pot_in_bets, ' | ', actions)
            if pot_in_bets.count(max(pot_in_bets)) == actions.count("RAISE") + actions.count("CALL") + actions.count("CHECK"):
                print(f"result: {result}")
                result = 'Next Round'
                break

    if result == 'Next Round':
        del GAME_ROUNDS[0]
        if len(GAME_ROUNDS) == 0:
            exit(f"La partida ha terminado. \nEl bote final es de {sum(pot_in_bets) + sum(pot_in_bets_arranged)}")
        positions, actions, pot_in_bets = adjustTable(positions, actions, pot_in_bets)
        roundDecisions(players_left, blinds, user_position, players_pockets, user_hand, positions, actions, pot_in_bets)
    else: 
        roundResult(pot_in_bets, actions, players_left, blinds, user_position, players_pockets, user_hand, positions)

def no_call_before_raise(actions):
    for accion in actions:
        if accion == 'RAISE':
            print("HA HABIDO RAISE")
            if 'CALL' in actions[:actions.index('RAISE')] or actions.count("RAISE") >= 1:
                print("HA HABIDO RAISE / CALL ANTES DE RAISE")
                return True
    return False

def adjustTable(positions, actions, pot_in_bets):
    global FALLEN_POT
    global positions_arranged
    global actions_arranged
    global pot_in_bets_arranged
    i = 0
    

    if FALLEN_POT == 0:
        inicio = positions.index('SB')
        empaquetado = list(zip(positions, actions, pot_in_bets))
        reordenado = empaquetado[inicio:] + empaquetado[:inicio]
        positions_arranged, actions_arranged, pot_in_bets_arranged = zip(*reordenado)
        positions_arranged = list(positions_arranged)
        actions_arranged = list(actions_arranged)
        pot_in_bets_arranged = list(pot_in_bets_arranged)

    while i < len(positions_arranged):
        if actions_arranged[i] == "FOLD":
            del positions_arranged[i]
            del actions_arranged[i]
            FALLEN_POT += pot_in_bets_arranged[i]
            del pot_in_bets_arranged[i]
        else:
            i += 1

    print(positions_arranged)
    print(actions_arranged)
    print(pot_in_bets_arranged)

    # while i < len(positions):
    #     if actions[i] == "FOLD":
    #         del positions[i]
    #         del actions[i]
    #         FALLEN_POT += pot_in_bets[i]
    #         del pot_in_bets[i]
    #     else:
    #         i += 1

    return positions_arranged, actions_arranged, pot_in_bets_arranged
        
