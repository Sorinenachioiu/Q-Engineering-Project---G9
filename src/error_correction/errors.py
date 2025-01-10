# Error definitions
def bit_flip_error(circuit, qubit):
    circuit.x(qubit)

def phase_flip_error(circuit, qubit):
    circuit.z(qubit)

def bit_phase_flip_error(circuit, qubit):
    circuit.y(qubit)

# Error registry (dictionary mapping error names to functions)
ERROR_TYPES = {
    "x": bit_flip_error, # x == bit_flip
    "z": phase_flip_error, # z == phase_flip
    "y": bit_phase_flip_error, # y == bit_phase_flip
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
    
    Args:
        circuit: QuantumCircuit object.
        errors: List of tuples (error_type, qubit) to apply.
    """

    if show_barriers: circuit.barrier()

    for error_type, qubit in errors:
        add_error(circuit, error_type, qubit)

    if show_barriers: circuit.barrier()
    
    return circuit


## HOW TO USE THE ABOVE FUNCTIONS
# 
# # Define circuit 
# circuit = QuantumCircuit(3)
# 
# # Define errors to apply: [(error_type, qubit), ...]
# errors = [("bit_flip", 0), ("phase_flip", 1), ("bit_phase_flip", 2)]
#
# # Apply multiple errors at the same time
# circuit = apply_errors(circuit, errors)