from connect import get_backend
from examples import *
from error_correction.examples.examples import *
from surface_codes.Steane import *
from surface_codes.four_two_two import *
from experiments.run_experiments import *
from run_ibm.four_two_two.four_two_two_ibm import *
from run_ibm.four_two_two.Deutsch import *

# set as "ibm" to use ibm backend
# backend_type = "ibm"
backend_type = "qi"

backend = get_backend(backend_type, True)


# if backend is None:
#     raise ValueError("Failed to retrieve IBM backend. Please check IBM credentials and configuration.")
# else:
#     run_422_on_ibm(backend)

# from run_ibm.four_two_two.results.interpret import *
# decode_measurement_results()


# Below to run all the deutsch logical 422 
# from run_ibm.four_two_two.four_two_two_qi import *
# run_Deutsch_logical_422_qi(backend)


# run_initial_examples(backend) # - run universal gate set and Grover
# basic_examples_simple_codes(backend) # - run error correction examples
# shor_code_examples(backend)

# counts = perform_experiment(backend, steane_code(), "surface/steane", shots=100)
# results = analyze_Steane_logical_state(counts)
# pretty_print_Steane_results(results)

experiments_to_run = ["x_422"]
run_experiments(backend, experiments_to_run)