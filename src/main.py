from connect import get_backend
from examples import *
from error_correction.examples.examples import *
# from basic_tic_tac_toe import *

# set as "ibm" to use ibm backend
# backend_type = "ibm"
backend_type = "qi"

backend = get_backend(backend_type, True)

# run_initial_examples(backend) # - run universal gate set and Grover
basic_examples_simple_codes(backend) # - run error correction examples
# shor_code_examples(backend)