from surface_codes.four_two_two import *
from surface_codes.Steane import *
from error_correction.basic_codes import *
from error_correction.Shor import *
from helpers import *

ERROR_CORRECTING_CODES = {
    "422": four_two_two_code,   # [[4,2,2]]
    "Steane": steane_code,      # [[7,1,3]]
    "513": bit_flip_error,      # [[5,1,3]]
    "Shor": shor_code           # [[9,1,3]]
}


RESULT_ANALYSIS = {
    "422": analyze_four_two_two_logical_state,      # [[4,2,2]]
    "Steane": analyze_four_two_two_logical_state,   # [[7,1,3]]
    "513": bit_flip_error,                          # [[5,1,3]]
    "Shor": shor_code                               # [[9,1,3]]
}

### Example errors
# errors = {
#     "target_qubits": [0],
#     "error_probs": {"x": 0.10, "z": 0.15, "y": 0.05}
# }


def four_two_two_experiment(backend, experiment_properties):
    
    base_errors = experiment_properties["base_errors"]                  # base error probabilities and target qubits
    runs_count = experiment_properties["runs_count"]                    # how many times to create the circuit for one error probability
    error_type = experiment_properties["error_type"]                    # what is the type of error that we want to modify
    error_range = experiment_properties["error_range"]                  # range of probability of errors
    number_of_samples = experiment_properties["number_of_samples"]      # how many sample probabilities to take from the range to test on
    shots = experiment_properties["shots"]                              # how many times to run a single experiment
    
    # take number_of_samples equally spaced values from the error_range interval 
    error_probabilities = np.linspace(error_range[0], error_range[1], number_of_samples)

    for error_probability in error_probabilities:
        current_errors = base_errors.copy()
        
        if error_type in current_errors["error_probs"]:
            current_errors["error_probs"][error_type] = error_probability

        for i in range(runs_count):
            experiment_name = f"errors/422/prob_{error_probability}/probabilistic_error_run_{i}"

            counts = perform_experiment(backend, ERROR_CORRECTING_CODES["422"]("00", current_errors), 
                                        experiment_name, store_results=False, shots=shots, verbose=True)
            
            results = RESULT_ANALYSIS["422"](counts)
            pretty_print_four_two_two_results(results)
