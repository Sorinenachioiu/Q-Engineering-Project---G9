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


def perform_four_two_two_experiment(backend, experiment_type, experiment_name, current_errors, shots):

    counts = perform_experiment(backend, ERROR_CORRECTING_CODES[experiment_type]("00", current_errors), 
                                experiment_name, store_results=False, shots=shots, verbose=False)
    
    results = RESULT_ANALYSIS[experiment_type](counts)
    pretty_print_four_two_two_results(results)

    return results

