from experiments.framework import *

def run_experiments(backend):
    experiment_properties = {
        "experiment_type": "422",
        "base_errors": {
            "target_qubits": [0, 1, 2, 3],
            "error_probs": {"x": 0.0, "z": 0.0, "y": 0.0}
        },
        "runs_count": 120,
        "error_type": "x",
        "error_range": (0.00, 0.41),
        "number_of_samples": 20,
        "shots": 4,
        "expected_state": "00",
    }
    qecc_experiment(backend, experiment_properties)