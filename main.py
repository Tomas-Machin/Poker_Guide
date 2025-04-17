from Logic.Game import PokerGame
#from Logic.Algorithms.Bayesian_Network import Network

from Logic.Information import info_registration
from Logic.Development import roundDecisions

if __name__ == "__main__":
    # inicio
    user_position, num_players, blinds, user_hand, players_pockets = info_registration()
    game = PokerGame(user_position, num_players, blinds, user_hand, players_pockets)
    game.start_game()
    # game.game_information()
    result = roundDecisions(num_players, blinds, user_position, players_pockets, user_hand, 0, 0, 0)
    print(f"El bote final es de {round(result, 2)}.")
    # INFORMACION DE CADA RONDA