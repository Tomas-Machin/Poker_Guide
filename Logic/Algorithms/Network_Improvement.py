import pandas as pd
import numpy as np
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

class PokerBayesianNetwork:
    POSITIONS = {"UTG": 0, "MP": 0, "HJ": 1, "CO": 1, "BU": 2, "SB": 2, "BB": 2}
    HAND_STRENGTHS = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}

    def __init__(self, user_position, user_chips, blinds, hand, active_players, model):
        self.user_position = user_position
        self.user_chips = user_chips
        self.blinds = blinds
        self.hand = hand
        self.active_players = active_players
        self.model = model  # Se puede pasar un modelo entrenado

    # --------------------------
    # Métodos de codificación
    # --------------------------
    def encode_position(self):
        return self.POSITIONS.get(self.user_position, 1)

    def encode_chips(self):
        ratio = float(self.user_chips) / float(self.blinds)
        return 0 if ratio < 5 else 1

    def encode_hand_strength(self):
        strong_cards = {"A", "K", "Q", "J", "10"}
        medium_cards = {"9", "8"}
        valores = [card[:-1] for card in self.hand]
        suits = [card[-1] for card in self.hand]
        suited = suits[0] == suits[1]
        strength = 0
        for val in valores:
            if val in strong_cards:
                strength += 1
            elif val in medium_cards:
                strength += 0.5
        if suited:
            strength += 0.5
        if strength <= 0.5:
            return self.HAND_STRENGTHS["LOW"]
        elif strength <= 1.5:
            return self.HAND_STRENGTHS["MEDIUM"]
        else:
            return self.HAND_STRENGTHS["HIGH"]

    def encode_active_players(self):
        if self.active_players < 2:
            return 0
        elif self.active_players < 4:
            return 1
        else:
            return 2

    # --------------------------
    # Entrenamiento desde CSV
    # --------------------------
    @staticmethod
    def entrenar_desde_csv(csv_path):
        df = pd.read_csv(csv_path, sep=';')

        # Mapear texto a numérico si está en formato legible
        mapeo = {
            'LOW': 0, 'MEDIUM': 1, 'HIGH': 2,
            'few': 0, 'moderate': 1, 'many': 2,
            'short': 0, 'deep': 1,
            'early': 0, 'middle': 1, 'late': 2,
            'Fold': 0, 'Check/Call': 1, 'Raise': 2
        }
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].map(mapeo)

        # Estructura de la red
        estructura = BayesianNetwork([
            ('HandStrength', 'WinProbability'),
            ('ActivePlayers', 'WinProbability'),
            ('ChipsInBlinds', 'WinProbability'),
            ('UserPosition', 'WinProbability')
        ])

        estructura.fit(df, estimator=MaximumLikelihoodEstimator)
        return estructura

    # --------------------------
    # Inferencia
    # --------------------------
    def infer_win_probability(self):
        if self.model is None:
            raise ValueError("No se ha entrenado o proporcionado un modelo.")

        infer = VariableElimination(self.model)

        evidence = {
            'HandStrength': self.encode_hand_strength(),
            'ActivePlayers': self.encode_active_players(),
            'ChipsInBlinds': self.encode_chips(),
            'UserPosition': self.encode_position()
        }

        result = infer.query(variables=['WinProbability'], evidence=evidence)
        return result

    def print_results(self):
        result = self.infer_win_probability()
        actions = ['Fold', 'Check/Call', 'Raise']
        print("\nProbabilidades estimadas para cada acción:")
        print("+------------+---------------------+")
        print("| Acción     | Probabilidad (phi)  |")
        print("+============+=====================+")
        for i, action in enumerate(actions):
            print(f"| {action:<10} | {result.values[i]:>19.4f} |")
        print("+------------+---------------------+")
