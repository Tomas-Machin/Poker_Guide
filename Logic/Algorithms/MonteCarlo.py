from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
import random
import numpy as np

class MonteCarloInference:
    def __init__(self, num_simulations=1000):
        self.num_simulations = num_simulations
        self.model = self._build_model()

    def _build_model(self):
        model = BayesianModel([('HandStrength', 'Action'),
                               ('Position', 'Action'),
                               ('Aggressiveness', 'Action')])

        cpd_hand = TabularCPD(variable='HandStrength', variable_card=3, values=[[0.33], [0.34], [0.33]])
        cpd_pos = TabularCPD(variable='Position', variable_card=2, values=[[0.5], [0.5]])
        cpd_aggr = TabularCPD(variable='Aggressiveness', variable_card=2, values=[[0.5], [0.5]])

        # Action: 0 = fold, 1 = check/call, 2 = raise
        cpd_action = TabularCPD(variable='Action', variable_card=3,
                                values=[
                                    # Weak hand
                                    [0.7, 0.5, 0.6, 0.4, 0.6, 0.4, 0.5, 0.3, 0.4, 0.2, 0.3, 0.1],
                                    [0.2, 0.3, 0.3, 0.4, 0.3, 0.4, 0.4, 0.4, 0.3, 0.4, 0.4, 0.4],
                                    [0.1, 0.2, 0.1, 0.2, 0.1, 0.2, 0.1, 0.3, 0.3, 0.4, 0.3, 0.5],
                                ],
                                evidence=['HandStrength', 'Position', 'Aggressiveness'],
                                evidence_card=[3, 2, 2])
        
        model.add_cpds(cpd_hand, cpd_pos, cpd_aggr, cpd_action)
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
                'HandStrength': random.randint(0, 2),       # 0 = weak, 1 = medium, 2 = strong
                'Position': random.randint(0, 1),           # 0 = early, 1 = late
                'Aggressiveness': random.randint(0, 1)      # 0 = passive, 1 = aggressive
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