from connect import get_backend
from examples import *
# from basic_tic_tac_toe import *

# set as "ibm" to use ibm backend
# backend_type = "ibm"
backend_type = "qi"

backend = get_backend(backend_type, True)

universal_gate_set(backend)

grovers_algorithm_smart(backend)

# play_tic_tac_toe()