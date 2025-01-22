from connect import get_backend
from examples import *
from error_correction.examples.examples import *
from surface_codes.Steane import *
from surface_codes.four_two_two import *
from experiments.run_experiments import *

# from basic_tic_tac_toe import *

# set as "ibm" to use ibm backend
# backend_type = "ibm"
backend_type = "qi"
# hi this is fun
backend = get_backend(backend_type, True)

# run_initial_examples(backend) # - run universal gate set and Grover
# basic_examples_simple_codes(backend) # - run error correction examples
# shor_code_examples(backend)

# counts = perform_experiment(backend, steane_code(), "surface/steane", shots=100)

# results = analyze_Steane_logical_state(counts)

# pretty_print_Steane_results(results)

run_experiments(backend)