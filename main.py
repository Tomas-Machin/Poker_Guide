from Logic.Game import PokerGame
from Logic.Information import info_registration
from Logic.Development import roundDecisions

if __name__ == "__main__":
    user_position, num_players, blinds, user_hand, players_pockets = info_registration()
    game = PokerGame(user_position, num_players, blinds, user_hand, players_pockets)
    game.start_game()
    roundDecisions(num_players, blinds, user_position, players_pockets, user_hand, [], [], [], [])