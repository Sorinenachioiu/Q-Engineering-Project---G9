

def x_flip_0_015_properites_422():
    return {
        "experiment_type": "422",
        "base_errors": {
            "target_qubits": [0, 1, 2, 3],
            "error_probs": {"x": 0.0, "z": 0.0, "y": 0.0}
        },
        "runs_count": 50,
        "error_types": ["x"],
        "error_range": (0.00, 0.25),
        "number_of_samples": 10,
        "shots": 4,
        "expected_state": "00",
        "experiment_path": "422/plots/x_flip",
    }


def y_flip_0_015_properites_422():
    return {
        "experiment_type": "422",
        "base_errors": {
            "target_qubits": [0, 1, 2, 3],
            "error_probs": {"x": 0.0, "z": 0.0, "y": 0.0}
        },
        "runs_count": 50,
        "error_types": ["y"],
        "error_range": (0.00, 0.25),
        "number_of_samples": 10,
        "shots": 4,
        "expected_state": "00",
        "experiment_path": "422/plots/y_flip",
    }


def z_flip_0_015_properites_422():
    return {
        "experiment_type": "422",
        "base_errors": {
            "target_qubits": [0, 1, 2, 3],
            "error_probs": {"x": 0.0, "z": 0.0, "y": 0.0}
        },
        "runs_count": 50,
        "error_types": ["z"],
        "error_range": (0.00, 0.25),
        "number_of_samples": 10,
        "shots": 4,
        "expected_state": "00",
        "experiment_path": "422/plots/z_flip",
    }

def all_flips_0_015_properties_422():
    return {
        "experiment_type": "422",
        "base_errors": {
            "target_qubits": [0, 1, 2, 3],
            "error_probs": {"x": 0.0, "z": 0.0, "y": 0.0}
        },
        "runs_count": 25,
        "error_types": ["x", "y", "z"],
        "error_range": (0.00, 0.15),
        "number_of_samples": 10,
        "shots": 4,
        "expected_state": "00",
        "experiment_path": "422/plots/xyz_flips",
    }