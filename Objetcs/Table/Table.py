import json

class Table:
    def __init__(self, num_players, blinds):
        self.positions = self.assign_positions(num_players)
        self.poker = {
            "Blinds": blinds,
            "Players": num_players,
            "Positions": {
                position: {"name": "Rival"} for position in self.positions
            }
        }

    def assign_positions(self, num_players):
        position_options = {
            2: ["SB", "BB"],                                # NO TENER EN CUENTA - es un 1v1
            3: ["BU", "SB", "BB"],                          # division 1-2 (posicion temprana-tardia)
            4: ["CO", "BU", "SB", "BB"],                    # division 1-1-2 / 2-2 (posicion temprana-media-tardia) (temprana-tardia)
            5: ["HJ", "CO", "BU", "SB", "BB"],              # division 2-1-2 (posicion temprana-media-tardia)
            6: ["MP", "HJ", "CO", "BU", "SB", "BB"],        # division 2-2-2 (posicion temprana-media-tardia)
            7: ["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]  # division 2-3-2 (posicion temprana-media-tardia)
        }
        return position_options.get(num_players, [])

    def get_table_info(self):
        return json.dumps(self.poker, indent=4)