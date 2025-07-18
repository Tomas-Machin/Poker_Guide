from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import numpy as np

class Network:
    def __init__(self, user_position, user_chips, blinds, hand, activePlayers):
        self.user_position = user_position
        self.user_chips = user_chips
        self.blinds = blinds
        self.hand = hand
        self.num_players = activePlayers

    def network_data(self):
        posiciones = {
            "UTG": 0,
            "MP": 0, 
            "HJ": 1, 
            "CO": 1, 
            "BU": 2,
            "SB": 2,
            "BB": 2 
        }

        posicion = posiciones[self.user_position]

        ciegas_tipo = 0 if float(self.user_chips) / float(self.blinds) < 5 else 1

        manos_fuertes = {"A", "K", "Q", "J", "10"}
        manos_intermedias = {"9", "8"}

        valores = [carta[:-1] for carta in self.hand]
        palos = [carta[-1] for carta in self.hand]

        suited = palos[0] == palos[1]

        potencial_mano = 0
        for valor in valores:
            if valor in manos_fuertes:
                potencial_mano += 1
            elif valor in manos_intermedias:
                potencial_mano += 0.5

        if suited:
            potencial_mano += 0.5  

        if potencial_mano <= 0.5:
            potencial_mano = 0
        elif potencial_mano <= 1.5:
            potencial_mano = 1
        else:
            potencial_mano = 2

        total_players = 0 if self.num_players < 2 else (1 if self.num_players < 4 else 2)

        return posicion, ciegas_tipo, potencial_mano, total_players

    def network(self):
        modelo = BayesianNetwork([
            ('HandStrength', 'WinProbability'),
            ('ActivePlayers', 'WinProbability'),
            ('ChipsInBlinds', 'WinProbability'),
            ('UserPosition', 'WinProbability')
        ])

        cpd_cartas_usuario = TabularCPD(variable='HandStrength', variable_card=3, values=[[0.3], [0.4], [0.3]])
        cpd_jugadores_activos = TabularCPD(variable='ActivePlayers', variable_card=3, values=[[0.2], [0.5], [0.3]])
        cpd_ciegas = TabularCPD(variable='ChipsInBlinds', variable_card=2, values=[[0.5], [0.5]])
        cpd_posicion_usuario = TabularCPD(variable='UserPosition', variable_card=3, values=[[0.33], [0.34], [0.33]])

        num_combinations = 3 * 3 * 2  * 3  
        values = np.random.rand(3, num_combinations)  
        values /= values.sum(axis=0)

        cpd_decision_usuario = TabularCPD(
            variable='WinProbability', variable_card=3,
            values=values,
            evidence=['HandStrength', 'ActivePlayers', 'ChipsInBlinds', 'UserPosition'], 
            evidence_card=[3, 3, 2, 3]
        )

        modelo.add_cpds(
            cpd_cartas_usuario, cpd_jugadores_activos, cpd_ciegas,
            cpd_posicion_usuario, cpd_decision_usuario
        )

        assert modelo.check_model()

        posicion, ciegas_tipo, potencial_mano, total_players = self.network_data()

        inferencia = VariableElimination(modelo)

        resultado = inferencia.query(
        variables=['WinProbability'], 
        evidence={'HandStrength': potencial_mano, 
                'ActivePlayers': total_players, 
                'ChipsInBlinds': ciegas_tipo, 
                'UserPosition': posicion}
        )

        return resultado

    def result_network(self):
        resultado = self.network()
        acciones = ['Fold', 'Check/Call', 'Raise']
        print("\nLas probabilidades de las jugadas son:")
        print("+--------------------+------------------------+")
        print("| WinProbability    |   phi(WinProbability) |")
        print("+====================+========================+")
        for i, accion in enumerate(acciones):
            print(f"| {accion:<18} | {resultado.values[i]:>22.4f} |")
        print("+--------------------+------------------------+")