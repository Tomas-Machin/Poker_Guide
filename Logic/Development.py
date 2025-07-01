from Logic.Algorithms.Bayesian_Network import Network
from Objects.Table.Table import Table

GAME_ROUNDS = ["PREFLOP", "POSTFLOP", "TURN", "RIVER"]
FALLEN_POT = 0
table_info = {}
positions_arranged = []
actions_arranged = []
pot_in_bets_arranged = []
communityCards = []

def roundDecisions(num_players, blinds, user_position, players_pockets, user_hand, positions, actions, pot_in_bets, round_bets):
    global table_info
    if GAME_ROUNDS[0] == 'PREFLOP':
        table_info = Table(num_players, blinds)
        positions = table_info.positions
    print(f"\nRonda {GAME_ROUNDS[0]}.")
    if GAME_ROUNDS[0] != 'PREFLOP':
        deal_community_cards()
    pot_in_bets, players_left, actions, round_bets = playerAction(num_players, blinds, user_position, players_pockets, user_hand, positions, actions, pot_in_bets, round_bets)
    roundResult(pot_in_bets, actions, players_left, blinds, user_position, players_pockets, user_hand, positions, round_bets)

def playerAction(num_players, blinds, user_position, players_pockets, user_hand, positions, actions, pot_in_bets, round_bets):
    players_left = 0
    if GAME_ROUNDS[0] == "PREFLOP":
        pot_in_bets, round_bets, actions = basePot_ActionsTable(num_players, blinds)

    for i in range(0, num_players):
        if (positions[i] == user_position):
            bynet = Network(user_position, players_pockets[user_position], blinds, user_hand, players_left)
            bynet.result_network()
        bet = input(f"\nCantidad de apuesta (vacío - FOLD) de la posicion: {positions[i]}: ")
        
        actions, pot_in_bets, players_left, round_bets = decisionResult(bet, actions, pot_in_bets, blinds, players_left, i, positions, round_bets)

    players_left = num_players - players_left
    
    return pot_in_bets, players_left, actions, round_bets

def basePot_ActionsTable(num_players, blinds):
    pot_in_bets = []
    round_bets = []
    actions = []
    for i in range(0, num_players):
        if i < num_players - 2:
            pot_in_bets.append(0)
            round_bets.append(0)
            actions.append('')
        elif i == num_players - 2 :            
            pot_in_bets.append(blinds/2)
            round_bets.append(0)
            actions.append('')
        else:
            pot_in_bets.append(blinds)
            round_bets.append(0)
            actions.append('')

    return pot_in_bets, round_bets, actions
        
def decisionResult(bet, actions, pot_in_bets, blinds, players_left, index, positions, round_bets):
    max_bet = 0
    if bet == '':
        actions[index] = "FOLD"
        players_left += 1
        print(f"Ha foldeado la posición: {positions[index]}.")
    else:
        if GAME_ROUNDS[0] == "PREFLOP":
            max_bet = max(pot_in_bets)
            if float(bet) == blinds/2 and max(pot_in_bets) == blinds and positions[index] == 'SB':
                pot_in_bets[index] = round(pot_in_bets[index] + float(bet), 2)
                actions[index] = "LIMP"
                print(f"Ha limpeado la posición: {positions[index]}.")
            elif float(bet) == 0 and max(pot_in_bets) == blinds and positions[index] == 'BB':
                pot_in_bets[index] = round(pot_in_bets[index] + float(bet), 2)
                actions[index] = "CHECK"
                print(f"Ha chequeado la posición: {positions[index]}.")
            elif round(float(bet) + pot_in_bets[index], 2) > max_bet:
                max_bet = float(bet)
                pot_in_bets[index] = round(pot_in_bets[index] + float(bet), 2)
                actions[index] = "RAISE"
                print(f"Ha raiseado la posición: {positions[index]}.")
            elif round(float(bet) + pot_in_bets[index], 2) == max_bet:
                pot_in_bets[index] = round(pot_in_bets[index] + float(bet), 2)
                actions[index] = "CALL"
                print(f"Ha calleado la posición: {positions[index]}.") 
            else:
                raise ValueError("La apuesta realizada no es valida.")  
        else:
            max_bet = max(round_bets)
            round_bets[index] = round(round_bets[index] + float(bet), 2)
            if (index == 0 and float(bet) == 0) or (float(bet) == 0 and round_bets[index - 1] == 0):
                actions[index] = "CHECK"
                print(f"Ha chequeado la posición: {positions[index]}.")
            elif round_bets[index] > max_bet:
                max_bet = float(bet)
                pot_in_bets[index] = round(pot_in_bets[index] + float(bet), 2)
                actions[index] = "RAISE"
                print(f"Ha raiseado la posición: {positions[index]}.")
            elif round_bets[index] == max(round_bets):
                pot_in_bets[index] = round(pot_in_bets[index] + float(bet), 2)
                actions[index] = "CALL"
                print(f"Ha calleado la posición: {positions[index]}.") 
            else:
                raise ValueError("La apuesta realizada no es valida.")
        
    
    return actions, pot_in_bets, players_left, round_bets

def roundResult(pot_in_bets, actions, players_left, blinds, user_position, players_pockets, user_hand, positions, round_bets):
    result = ''
    if actions.count("FOLD") == len(positions):
        exit("La partida ha terminado sin ganador.")
    elif actions.count("CALL") == 1 and actions.count("FOLD") == len(actions) - 1:
        print(f"Ha ganado la posición {positions[actions.index("CALL")]}.")
    elif actions.count("RAISE") == 1 and actions.count("FOLD") == len(actions) - 1:
        print(f"Ha ganado la posición {positions[actions.index("RAISE")]}.")
    elif no_call_before_raise(actions) == False:
        result = 'Next Round'
    else:    
        print("\nSe vuelven a tomar decisiones.")
        for i in range(0, len(actions)):
            if pot_in_bets[i] < max(pot_in_bets) and actions[i] != "FOLD":
                if (positions[i] == user_position):
                    bynet = Network(user_position, players_pockets[user_position], blinds, user_hand, players_left)
                    bynet.result_network()
                bet = input(f"\nCantidad de apuesta (vacío - FOLD) de la posicion: {positions[i]}: ")
                actions, pot_in_bets, players_left, round_bets = decisionResult(bet, actions, pot_in_bets, blinds, players_left, i, positions, round_bets)
                print(pot_in_bets, ' | ', actions)
            if pot_in_bets.count(max(pot_in_bets)) == actions.count("RAISE") + actions.count("CALL") + actions.count("CHECK"):
                result = 'Next Round'
                break

    if result == 'Next Round':
        del GAME_ROUNDS[0]
        if len(GAME_ROUNDS) == 0:
            print(f"\nLa partida ha terminado. \nEl bote final es de {round(FALLEN_POT + sum(pot_in_bets_arranged), 2)}")  # mal -> suma doble en casos sin folds
            return
        if GAME_ROUNDS[0] == "POSTFLOP": positions, actions, pot_in_bets = adjustTable(positions, actions, pot_in_bets)
        roundDecisions(players_left, blinds, user_position, players_pockets, user_hand, positions, actions, pot_in_bets, round_bets)
    else: 
        roundResult(pot_in_bets, actions, players_left, blinds, user_position, players_pockets, user_hand, positions, round_bets)

def no_call_before_raise(actions):
    for accion in actions:
        if accion == 'RAISE':
            if 'CALL' in actions[:actions.index('RAISE')] or actions.count("RAISE") >= 1:
                return True
    return False

def adjustTable(positions, actions, pot_in_bets):
    global FALLEN_POT
    global positions_arranged
    global actions_arranged
    global pot_in_bets_arranged
    i = 0

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

    return positions_arranged, actions_arranged, pot_in_bets_arranged
        
def deal_community_cards():
    global communityCards
    if GAME_ROUNDS[0] == "POSTFLOP":
        communityCards = input(f"\nCartas comunitarias de la ronda POSTFLOP: ").upper().split()
        table_info.poker["Community cards"] = communityCards
    elif GAME_ROUNDS[0] == "TURN":
        forthCard = input(f"\nCarta comunitaria de la ronda TURN: ").upper()
        communityCards.append(forthCard)
        table_info.poker["Community cards"] = communityCards
    if GAME_ROUNDS[0] == "RIVER":
        fifthCard = input(f"\nCarta comunitaria de la ronda RIVER: ").upper()
        communityCards.append(fifthCard)
        table_info.poker["Community cards"] = communityCards