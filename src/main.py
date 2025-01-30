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

# from laflamme import *
# counts = perform_experiment(backend, generate_laflamme_circuit(init_state=False), "laflamme/with_recovery_1_init", shots=1024)
# results = analyze_laflamme_logical_state(counts)
# pretty_print_laflamme_results(results)


############# EXPERIMENTS #######################
## Remember to change in helpers the ylim part
# experiments_to_run = ["x_513"]
# experiments_to_run = ["y_513"]
# experiments_to_run = ["z_513"]
# run_experiments(backend, experiments_to_run)

# perform_experiment(backend, generate_stabilizers_x_circuit_steane(), "steane/stabilizers/x" )
# perform_experiment(backend, generate_stabilizers_z_circuit_steane(), "steane/stabilizers/z" )

# perform_experiment(backend, bit_flip_code(), "presentation/basic_bit_flip" )
perform_experiment(backend, four_two_two_Deutsch_f11_constant(), "deutsch/f11_const" )

# q = QuantumRegister(9,'q')
# c = ClassicalRegister(1,'c')

# circuit = QuantumCircuit(q, c)
# perform_experiment(backend, shor_encoding(circuit, q), "presentation/shor_encoding" )