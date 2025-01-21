from connect import get_backend
from examples import *
from error_correction.examples.examples import *
# from basic_tic_tac_toe import *

# set as "ibm" to use ibm backend
# backend_type = "ibm"
backend_type = "qi"
# hi this is fun
backend = get_backend(backend_type, True)

universal_gate_set(backend)

grovers_algorithm(backend)

# play_tic_tac_toe()