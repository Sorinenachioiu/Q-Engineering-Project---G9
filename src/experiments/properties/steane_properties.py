

def x_flip_0_005_properites_steane():
    return {
        "experiment_type": "Steane",
        "base_errors": {
            "target_qubits": [0, 1, 2, 3, 4, 5, 6],
            "error_probs": {"x": 0.0, "z": 0.0, "y": 0.0}
        },
        "runs_count": 100,
        "error_types": ["x"],
        "error_range": (0.00, 0.05),
        "number_of_samples": 10,
        "shots": 4,
        "expected_state": "0",
        "experiment_path": "Steane/plots/x_flip",
    }


def y_flip_0_005_properites_steane():
    return {
        "experiment_type": "Steane",
        "base_errors": {
            "target_qubits": [0, 1, 2, 3, 4, 5, 6],
            "error_probs": {"x": 0.0, "z": 0.0, "y": 0.0}
        },
        "runs_count": 100,
        "error_types": ["y"],
        "error_range": (0.00, 0.05),
        "number_of_samples": 10,
        "shots": 4,
        "expected_state": "0",
        "experiment_path": "Steane/plots/y_flip",
    }

def z_flip_0_005_properites_steane():
    return {
        "experiment_type": "Steane",
        "base_errors": {
            "target_qubits": [0, 1, 2, 3, 4, 5, 6],
            "error_probs": {"x": 0.0, "z": 0.0, "y": 0.0}
        },
        "runs_count": 100,
        "error_types": ["z"],
        "error_range": (0.00, 0.05),
        "number_of_samples": 10,
        "shots": 4,
        "expected_state": "0",
        "experiment_path": "Steane/plots/z_flip",
    }