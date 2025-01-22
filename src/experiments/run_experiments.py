from experiments.framework import *

def run_experiments(backend):
    experiment_properties = {
        "base_errors": {
            "target_qubits": [0, 1, 2, 3],
            "error_probs": {"x": 0.0, "z": 0.0, "y": 0.0}
        },
        "runs_count": 10,
        "error_type": "x",
        "error_range": (0.00, 0.10),
        "number_of_samples": 10,
        "shots": 10
    }
    four_two_two_experiment(backend, experiment_properties)