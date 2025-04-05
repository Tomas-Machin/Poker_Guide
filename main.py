from Logic.Game import PokerGame
from Logic.Bayesian_Network import Network

from Logic.Info_Entry import info_registration

if __name__ == "__main__":
    # inicio
    user_position, num_players, blinds, user_hand, players_pockets = info_registration()
    game = PokerGame(user_position, num_players, blinds, user_hand, players_pockets)
    game.start_game()
    game.game_information()