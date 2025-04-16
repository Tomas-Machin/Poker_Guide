POKER_POSITIONS = ["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]

def playerDecision(num_players, blinds):

    pot_in_bets, players_left, actions = playerAction(num_players, blinds)  # first round decision

    roundResult(num_players, pot_in_bets, actions, players_left, blinds)            

def playerAction(num_players, blinds):
    players_left = 0

    pot_in_bets, actions = basePot_ActionsTable(num_players, blinds)

    for i in range(0, num_players):
        bet = input(f"Cantidad de apuesta (vacío - FOLD) de la posicion: {POKER_POSITIONS[i]}: ")
        
        actions, pot_in_bets, players_left = decisionResult(bet, actions, pot_in_bets, blinds, i)
                
        print(pot_in_bets, ' | ', actions)
        players_left = num_players - players_left
    
    return pot_in_bets, players_left, actions

def basePot_ActionsTable(num_players, blinds):
    pot_in_bets = []
    actions = []
    for i in range(0, num_players):
        if(i < num_players - 2):
            pot_in_bets.append(0)
            actions.append('')
        elif(i == num_players - 2):            
            pot_in_bets.append(blinds/2)
            actions.append('')
        else:
            pot_in_bets.append(blinds)
            actions.append('')

    return pot_in_bets, actions
        
def decisionResult(bet, actions, pot_in_bets, blinds, i):
    max_bet = blinds
    if bet == '':
        actions[i] = "FOLD"
        players_left += 1
        print(f"Ha foldeado la posición: {POKER_POSITIONS[i]}.")
    elif float(bet) == blinds/2 and max(pot_in_bets) == blinds and POKER_POSITIONS[i] == 'SB':
        actions[i] = "CALL"
        print(f"Ha calleado la posición: {POKER_POSITIONS[i]}.")
    elif float(bet) == 0 and max(pot_in_bets) == blinds and POKER_POSITIONS[i] == 'BB':
        actions[i] = "CALL"
        print(f"Ha calleado la posición: {POKER_POSITIONS[i]}.")
    elif float(bet) == max_bet:
        pot_in_bets[i] += float(bet)
        actions[i] = "CALL"
        print(f"Ha calleado la posición: {POKER_POSITIONS[i]}.") 
    elif float(bet) > max_bet:
        max_bet = float(bet)
        pot_in_bets[i] += float(bet)
        actions[i] = "RAISE"
        print(f"Ha raiseado la posición: {POKER_POSITIONS[i]}.")
    else:
        exit("La apuesta realizada no es valida.")      
        # dejar tomar la decision otra vez?    
    
    return actions, pot_in_bets, players_left

def nextRound():
    return

def roundResult(num_players, pot_in_bets, actions, players_left, blinds):
    if POKER_POSITIONS.count("CALL") == 1:
        print(f"Ha ganado la posición {POKER_POSITIONS[actions.index("CALL")]}.")
    elif POKER_POSITIONS.count("RAISE") == 1:
        print(f"Ha ganado la posición {POKER_POSITIONS[actions.index("RAISE")]}.")
    elif(pot_in_bets[i] < max(pot_in_bets) and actions[i] != "FOLD"):
        for i in range(0, num_players):
            bet = input(f"Cantidad de apuesta (vacío - FOLD) de la posicion: {POKER_POSITIONS[i]}: ")
            actions, pot_in_bets, players_left = decisionResult(bet, actions, pot_in_bets, blinds, i)
            roundResult(num_players, pot_in_bets, actions, players_left, blinds)
    else:
        nextRound(pot_in_bets, players_left)