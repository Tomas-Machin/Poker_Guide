import json
from Objects.Round.Round import Round

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return super().default(obj)

class Table:
    def __init__(self, num_players, blinds):
        self.positions = self.assign_positions(num_players)
        self.poker = {
            "Blinds": blinds,
            "TotalPlayers": num_players,
            "Positions": {
                position: {"name": "Rival"} for position in self.positions
            },
            "Round": Round([], blinds, num_players)
        }

    def assign_positions(self, num_players):
        position_options = {
            2: ["SB", "BB"],
            3: ["BU", "SB", "BB"],
            4: ["CO", "BU", "SB", "BB"],
            5: ["HJ", "CO", "BU", "SB", "BB"],
            6: ["MP", "HJ", "CO", "BU", "SB", "BB"],
            7: ["UTG", "MP", "HJ", "CO", "BU", "SB", "BB"]
        }
        return position_options.get(num_players, [])

    def get_table_info(self):
        poker_copy = self.poker.copy()

        # Obtener el contenido del Round
        round_data = self.poker["Round"].__dict__

        # Si dentro de Round hay una clave 'ronda', usamos su contenido directamente
        if "ronda" in round_data and isinstance(round_data["ronda"], dict):
            poker_copy["Round"] = round_data["ronda"]
        else:
            poker_copy["Round"] = round_data

        return json.dumps(poker_copy, indent=4)
