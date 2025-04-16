from Logic.Game import PokerGame
#from Logic.Algorithms.Bayesian_Network import Network

from Logic.Information import info_registration, firstDecision

if __name__ == "__main__":
    # inicio
    user_position, num_players, blinds, user_hand, players_pockets = info_registration()
    game = PokerGame(user_position, num_players, blinds, user_hand, players_pockets)
    game.start_game()
    pot_in_bets, players_left = firstDecision(num_players, blinds)
    #game.game_information()