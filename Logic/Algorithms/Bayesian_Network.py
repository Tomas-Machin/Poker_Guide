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
        # Posición del usuario
        posiciones = {
            "UTG": 0,  # Temprana
            "MP": 0,   # Temprana
            "HJ": 1,   # Media
            "CO": 1,   # Media
            "BU": 2,   # Tardía
            "SB": 2,   # Tardía
            "BB": 2    # Tardía
        }

        posicion = posiciones[self.user_position]

        # Dependiendo del valor de la ciega, determinamos si son altas o bajas -> si no puedes jugar 5 manos | 10 manos
        ciegas_tipo = 0 if float(self.user_chips) / float(self.blinds) < 5 else 1

        # Mapeamos la mano a categorías de "Débil", "Media" o "Fuerte"
        # evaluar la mano como conjunto de max 4 y menos 0 y de ahi evaluar alto-medio-bajo
        manos_fuertes = {"A", "K", "Q", "J", "10"}
        manos_intermedias = {"9", "8"}

        # Separar valores y palos de las cartas
        valores = [carta[:-1] for carta in self.hand]
        palos = [carta[-1] for carta in self.hand]

        # Verificar si la mano es suited (mismo palo)
        suited = palos[0] == palos[1]

        # Evaluar fuerza de la mano
        potencial_mano = 0
        for valor in valores:
            if valor in manos_fuertes:
                potencial_mano += 1
            elif valor in manos_intermedias:
                potencial_mano += 0.5

        # Ajuste si es suited
        if suited:
            potencial_mano += 0.5  # Bonificación si las cartas son del mismo palo

        # Normalizar a 0 (débil), 1 (media), 2 (fuerte)
        if potencial_mano <= 0.5:
            potencial_mano = 0
        elif potencial_mano <= 1.5:
            potencial_mano = 1
        else:
            potencial_mano = 2

        total_players = 0 if self.num_players < 2 else (1 if self.num_players < 4 else 2)

        return posicion, ciegas_tipo, potencial_mano, total_players

    def network(self):
        # Definir la estructura del modelo
        modelo = BayesianNetwork([
            ('CartasUsuario', 'DecisionUsuario'),
            ('JugadoresActivos', 'DecisionUsuario'),
            ('Ciegas', 'DecisionUsuario'),
            #('FichasUsuario', 'DecisionUsuario'),
            ('PosicionUsuario', 'DecisionUsuario')
        ])

        # Definir las distribuciones de probabilidad condicional (CPDs)
        cpd_cartas_usuario = TabularCPD(variable='CartasUsuario', variable_card=3, values=[[0.3], [0.4], [0.3]])
        cpd_jugadores_activos = TabularCPD(variable='JugadoresActivos', variable_card=3, values=[[0.2], [0.5], [0.3]])
        cpd_ciegas = TabularCPD(variable='Ciegas', variable_card=2, values=[[0.5], [0.5]])
        #cpd_fichas_usuario = TabularCPD(variable='FichasUsuario', variable_card=3, values=[[0.3], [0.4], [0.3]])
        cpd_posicion_usuario = TabularCPD(variable='PosicionUsuario', variable_card=3, values=[[0.33], [0.34], [0.33]])

        # Generar una matriz de probabilidad aleatoria válida para DecisionUsuario
        num_combinations = 3 * 3 * 2  * 3  # 162 combinaciones posibles de entrada
        values = np.random.rand(3, num_combinations)  # Matriz de valores aleatorios
        values /= values.sum(axis=0)  # Normalizar para que cada columna sume 1

        cpd_decision_usuario = TabularCPD(
            variable='DecisionUsuario', variable_card=3,
            values=values,
            evidence=['CartasUsuario', 'JugadoresActivos', 'Ciegas', 'PosicionUsuario'], #'FichasUsuario', 'PosicionUsuario'],
            evidence_card=[3, 3, 2, 3]
        )

        # Agregar CPDs al modelo
        modelo.add_cpds(
            cpd_cartas_usuario, cpd_jugadores_activos, cpd_ciegas, #cpd_fichas_usuario, 
            cpd_posicion_usuario, cpd_decision_usuario
        )

        # Comprobar si la red es válida
        assert modelo.check_model()

        posicion, ciegas_tipo, potencial_mano, total_players = self.network_data()

        # Realizar inferencia en la red
        inferencia = VariableElimination(modelo)

        resultado = inferencia.query(
        variables=['DecisionUsuario'], 
        evidence={'CartasUsuario': potencial_mano, 
                'JugadoresActivos': total_players, 
                #'Ciegas': table_info.poker["Blinds"], 
                'Ciegas': ciegas_tipo, 
                'PosicionUsuario': posicion}
        )

        return resultado

    def result_network(self):
        resultado = self.network()
        # Reemplazar valores numéricos por etiquetas
        acciones = ['Fold', 'Check/Call', 'Raise']
        print("\nLas probabilidades de las jugadas son:")
        print("+--------------------+------------------------+")
        print("| DecisionUsuario    |   phi(DecisionUsuario) |")
        print("+====================+========================+")
        for i, accion in enumerate(acciones):
            print(f"| {accion:<18} | {resultado.values[i]:>22.4f} |")
        print("+--------------------+------------------------+")

        #------------------------------------------------------------------------------
        # añadir termino medio a las ciegas del jugador 5 - 10 - +10
        # quitar las fichas de usuario -> se tiene en cuenta en las ciegas