from experiments.experiments import *
import matplotlib.pyplot as plt
from helpers import *
import time

EXPERIMENT_TYPE = {
    "422": perform_four_two_two_experiment,
}

### Example errors
# errors = {
#     "target_qubits": [0],
#     "error_probs": {"x": 0.10, "z": 0.15, "y": 0.05}
# }


def qecc_experiment(backend, experiment_properties):
    start_time = time.time()  # Start timing the experiment

    experiment_type = experiment_properties["experiment_type"]
    base_errors = experiment_properties["base_errors"]                  # base error probabilities and target qubits
    runs_count = experiment_properties["runs_count"]                    # how many times to create the circuit for one error probability
    error_types = experiment_properties["error_types"]                    # what is the type of error that we want to modify
    error_range = experiment_properties["error_range"]                  # range of probability of errors
    number_of_samples = experiment_properties["number_of_samples"]      # how many sample probabilities to take from the range to test on
    shots = experiment_properties["shots"]                              # how many times to run a single experiment
    expected_state = experiment_properties["expected_state"]
    experiment_path = experiment_properties["experiment_path"]
    
    # take number_of_samples equally spaced values from the error_range interval 
    error_probabilities = np.linspace(error_range[0], error_range[1], number_of_samples)

    success_rates = []

    for error_probability in error_probabilities:
        current_errors = base_errors.copy()
        
        for error_type in error_types:
            if error_type in current_errors["error_probs"]:
                current_errors["error_probs"][error_type] = error_probability

        success_count = 0

        for i in range(runs_count):

            experiment_name = f"errors/{experiment_type}/prob_{error_probability}/probabilistic_error_run_{i}"

            results = EXPERIMENT_TYPE[experiment_type](backend, experiment_type, experiment_name, current_errors, shots)

            if results['deduced_state'] == expected_state:
                success_count += 1

        success_rate = success_count / runs_count
        success_rates.append(success_rate)

        print(f"Error Probability: {error_probability:.2f}, Success Rate: {success_rate:.2%}")

    experiment_name = f"{experiment_type}"
    save_experiment_plot(error_probabilities, success_rates, experiment_name, experiment_path)

    end_time = time.time()  
    total_time = end_time - start_time
    print(f"Total experiment runtime: {total_time:.2f} seconds")

