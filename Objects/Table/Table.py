import json

class Table:
    def __init__(self, num_players, blinds):
        self.positions = self.assign_positions(num_players)
        self.poker = {
            "Blinds": blinds,
            "Players": num_players,
            "Community cards": [],
            "Positions": {
                position: {"name": "Rival"} for position in self.positions
            }
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
        return json.dumps(self.poker, indent=4)