from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from itertools import combinations
import numpy as np

class MonteCarloInference:
    def __init__(self, position, chips, table_blinds, player_cards, activePlayers, num_simulations=1000):
        """
        Constructor que recibe los datos del jugador y la mesa.
        
        :param position: Posición del jugador (0 = temprana, 1 = media, 2 = tardía)
        :param blinds: Ciegas del jugador, como la fracción de fichas en relación con las ciegas de la mesa
        :param hand: Fuerza de la mano del jugador (0 = débil, 1 = media, 2 = fuerte)
        :param players_in_pot: Cantidad de jugadores que han apostado hasta el turno del jugador
        :param num_simulations: Número de simulaciones de Monte Carlo a realizar
        """
        self.position = position
        self.blinds = round(float(chips) / float(table_blinds), 2)
        self.player_cards = player_cards
        self.community_cards = []   # community_cards
        self.players_in_pot = activePlayers
        self.num_simulations = num_simulations

        self.hand = self.evaluate_hand(self.player_cards, self.community_cards)
        self.model = self._build_model()

    # Función para evaluar la fuerza de la mano
    def evaluate_hand(self, player_cards, community_cards):
        # Definir los valores de las cartas y los palos
        RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        SUITS = ['S', 'C', 'D', 'H']  # Espadas, Corazones, Diamantes, Tréboles
        """
        Evaluar la fuerza de la mano del jugador basándose en las cartas del jugador y las comunitarias.
        
        :param player_cards: Cartas del jugador en formato ["AS", "AC"]
        :param community_cards: Cartas comunitarias en formato ["10S", "JH", "QD", "7C", "3D"]
        :return: Fuerza de la mano (0 = débil, 1 = media, 2 = fuerte)
        """
        all_cards = player_cards + community_cards
        hand_strength = 0

        # Combinaciones posibles de cinco cartas
        five_card_hands = list(combinations(all_cards, 5))
        
        for hand in five_card_hands:
            values = [card[:-1] for card in hand]  # Extraer solo el valor (sin palo)
            suits = [card[-1] for card in hand]   # Extraer el palo (último carácter)

            # Comprobar si es un color (todas las cartas del mismo palo)
            if len(set(suits)) == 1:
                hand_strength += 1  # Color
                continue
            
            # Comprobar si es una escalera (cartas consecutivas)
            sorted_values = sorted([RANKS.index(v) for v in values])
            if sorted_values == list(range(sorted_values[0], sorted_values[0] + 5)):
                hand_strength += 1  # Escalera
                continue

            # Comprobar otras combinaciones (pares, tríos, full house, etc.)
            value_counts = {v: values.count(v) for v in values}
            if 4 in value_counts.values():  # Cuatro de un tipo
                hand_strength += 2
            elif 3 in value_counts.values() and 2 in value_counts.values():  # Full house
                hand_strength += 2
            elif 3 in value_counts.values():  # Trío
                hand_strength += 1
            elif 2 in value_counts.values():  # Par
                hand_strength += 0.5

        # Si la mano es un color o una escalera, es fuerte
        if hand_strength > 1:
            return 2  # Mano fuerte
        elif hand_strength > 0:
            return 1  # Mano media
        else:
            return 0  # Mano débil

    # # Ejemplo de uso
    # player_cards = ["AS", "AC"]  # As y As de espadas
    # community_cards = ["10S", "JH", "QD", "7C", "3D"]

    # hand_strength = evaluate_hand(player_cards, community_cards)

    # # La función devolverá 2 para una mano fuerte (pareja de Ases)
    # print("Fuerza de la mano:", hand_strength)

    def _build_model(self):
        model = BayesianNetwork([('HandStrength', 'Action'),
                               ('Position', 'Action'),
                               ('Blinds', 'Action'),
                               ('PlayersInPot', 'Action')])

        # Probabilidades de la mano (fuerza de la mano)
        cpd_hand = TabularCPD(variable='HandStrength', variable_card=3, values=[[0.5], [0.3], [0.2]])

        # Probabilidades de la posición (temprana, media, tardía)
        cpd_pos = TabularCPD(variable='Position', variable_card=3, values=[[0.33], [0.34], [0.33]])

        # Probabilidades de las ciegas (pueden depender de cuántas fichas tiene el jugador)
        cpd_blinds = TabularCPD(variable='Blinds', variable_card=2, values=[[0.5], [0.5]])

        # Probabilidades de los jugadores en el bote (esto afecta las decisiones del jugador)
        cpd_pot = TabularCPD(variable='PlayersInPot', variable_card=7, values=[[0.14], [0.14], [0.14], [0.16], [0.14], [0.14], [0.14]])

        # Probabilidades de la acción (fold, check/call, raise)
        values = []
        for i in range(126):
            # Probabilidades arbitrarias para cada combinación de evidencia.
            # Estas probabilidades deben sumar 1 para cada fila.
            values.append([0.3, 0.4, 0.3])  # Por ejemplo: [pasar, subir, subir mucho]
        
        # Convertir los valores a la forma (3, 126) usando zip y la transposición de las listas.
        values_transposed = list(zip(*values))  # Esto intercambia las filas con las columnas

        # Crear la CPD para la variable 'Action'
        cpd_action = TabularCPD(variable='Action', variable_card=3,
                                values=values_transposed,  # Ahora tiene la forma (3, 126)
                                evidence=['HandStrength', 'Position', 'Blinds', 'PlayersInPot'],
                                evidence_card=[3, 3, 2, 7])

        model.add_cpds(cpd_hand, cpd_pos, cpd_blinds, cpd_pot, cpd_action)
        model.check_model()
        return model

    def infer_action_probabilities(self, evidence):
        inference = VariableElimination(self.model)
        result = inference.query(variables=['Action'], evidence=evidence)
        return result.values

    def run_monte_carlo(self):
        fold, call, raise_ = 0, 0, 0
        for _ in range(self.num_simulations):
            evidence = {
                'HandStrength': self.hand,                    # 0 = weak, 1 = medium, 2 = strong
                'Position': self.position,                    # 0 = early, 1 = middle, 2 = late
                'Blinds': int(self.blinds > 50),             # 0 = low, 1 = high
                'PlayersInPot': min(self.players_in_pot, 4),  # Número de jugadores (max 4 para simplificar)
            }
            probs = self.infer_action_probabilities(evidence)
            action = np.argmax(probs)
            if action == 0:
                fold += 1
            elif action == 1:
                call += 1
            else:
                raise_ += 1

        total = self.num_simulations
        return {
            'fold': fold / total,
            'check/call': call / total,
            'raise': raise_ / total
        }
