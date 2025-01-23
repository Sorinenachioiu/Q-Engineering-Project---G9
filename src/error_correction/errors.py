import numpy as np

# Error definitions
def bit_flip_error(circuit, qubit):
    circuit.x(qubit)
    return circuit

def phase_flip_error(circuit, qubit):
    circuit.z(qubit)
    return circuit

def bit_phase_flip_error(circuit, qubit):
    circuit.y(qubit)
    return circuit

def identity(circuit, qubit):
    circuit.id(qubit)
    return circuit 

# Error registry (dictionary mapping error names to functions)
ERROR_TYPES = {
    "x": bit_flip_error, # x == bit_flip
    "z": phase_flip_error, # z == phase_flip
    "y": bit_phase_flip_error, # y == bit_phase_flip
    "i": identity
}

def add_error(circuit, error_type, qubit_number):
    """Apply an error to a quantum circuit."""
    if error_type in ERROR_TYPES:
        ERROR_TYPES[error_type](circuit, qubit_number)
    else:
        raise ValueError(f"Error type '{error_type}' not recognized.")
    return circuit


def apply_errors(circuit, errors, show_barriers = True):
    """
    Apply a sequence of errors to a quantum circuit.
    The errors are predefined and passed as arguments
    
    Args:
        circuit: QuantumCircuit object.
        errors: List of tuples (error_type, qubit) to apply.
    """

    if show_barriers: circuit.barrier()

    for error_type, qubit in errors:
        add_error(circuit, error_type, qubit)

    if show_barriers: circuit.barrier()
    
    return circuit


def apply_errors_probabilistic(circuit, qubits, error_probabilities, show_barriers=True):
    """
    Apply probabilistic errors to a region of the quantum circuit.

    Args:
        circuit: QuantumCircuit object.
        qubits: List of qubits to apply errors to.
        error_probabilities: Dictionary with error types as keys and their probabilities as values.
                            Example: {"x": 0.10, "z": 0.15, "y": 0.05}
        show_barriers: Boolean indicating whether to add barriers before and after errors.
    
    Returns:
        circuit: Updated quantum circuit with errors applied.
    """
    if show_barriers:
        circuit.barrier()

    # Create a list of error types and their corresponding probabilities
    error_types = list(error_probabilities.keys())
    probabilities = list(error_probabilities.values())

    # Add identity with probability to ensure total = 1
    if "i" not in error_probabilities:
        error_types.append("i")
        probabilities.append(1 - sum(probabilities))

    for qubit in qubits:
        error_choice = np.random.choice(error_types, p=probabilities)
        add_error(circuit, error_choice, qubit)

    if show_barriers:
        circuit.barrier()

    return circuit


## HOW TO USE THE ABOVE FUNCTIONS ###
# 
# # Define circuit 
# circuit = QuantumCircuit(3)
# 
# # Define errors to apply: [(error_type, qubit), ...]
# errors = [("bit_flip", 0), ("phase_flip", 1), ("bit_phase_flip", 2)]
#
# # Apply multiple errors at the same time
# circuit = apply_errors(circuit, errors)

### How to use the probabilistic one ###
#
# # Define qubits to apply errors on
# target_qubits = [0, 1, 2]
#
# # Define error probabilities (10% bit-flip, 15% phase-flip, 5% bit-phase-flip) , p_identity = 1-sum(error_probabilities)
# error_probs = {"x": 0.10, "z": 0.15, "y": 0.05}
#
# # Apply probabilistic errors
# qc = apply_errors_probabilistic(qc, target_qubits, error_probs)


##
# Page 460 the probability that we would expect for p = bit flip probability
# 3*p^2 - 2* p^3
# https://profmcruz.wordpress.com/wp-content/uploads/2017/08/quantum-computation-and-quantum-information-nielsen-chuang.pdf
