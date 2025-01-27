# experiment_type - the code that we want to test
# base_errors - initial assumptions about errors
# target_qubits - the qubits that can be affected by errors
# error_probability - the probability of an error occuring for each type of error
# runs_count - the number of time we create the circuit and run it
# error_types - specifies what types of errors we want to modify during the experiment
# error_range - the range of error probabilities that we want to test
# number_of_samples - the amount of equally spaced points in the error_range that define the error probabilities that we want to test. (e.g range = (0, 0.1), number_of_samples = 3 => we take three points 0, 0.05, 0.1 and run experiments for each of them)
# shots - amount of times we repeat an experiment with the same circuit
# expected_state - the state that we expect to get as result
# experiment_path - where we want to save the results of the experiment

def x_flip_0_014_properites_513():
    return {
        "experiment_type": "513",
        "base_errors": {
            "target_qubits": [0, 1, 2, 3, 4],
            "error_probs": {"x": 0.0, "z": 0.0, "y": 0.0}
        },
        "runs_count": 100,
        "error_types": ["x"],
        "error_range": (0.00, 0.14),
        "number_of_samples": 10,
        "shots": 1,
        "expected_state": "0",
        "experiment_path": "513/plots/x_flip",
    }


def y_flip_0_014_properites_513():
    return {
        "experiment_type": "513",
        "base_errors": {
            "target_qubits": [0, 1, 2, 3, 4],
            "error_probs": {"x": 0.0, "z": 0.0, "y": 0.0}
        },
        "runs_count": 100,
        "error_types": ["y"],
        "error_range": (0.00, 0.14),
        "number_of_samples": 10,
        "shots": 1,
        "expected_state": "0",
        "experiment_path": "513/plots/y_flip",
    }


def z_flip_0_014_properites_513():
    return {
        "experiment_type": "513",
        "base_errors": {
            "target_qubits": [0, 1, 2, 3, 4],
            "error_probs": {"x": 0.0, "z": 0.0, "y": 0.0}
        },
        "runs_count": 100,
        "error_types": ["z"],
        "error_range": (0.00, 0.14),
        "number_of_samples": 10,
        "shots": 1,
        "expected_state": "0",
        "experiment_path": "513/plots/z_flip",
    }
