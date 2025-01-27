from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from error_correction.errors import *


def steane_apply_X_logical(circuit, data):
    for i in range(7):
        circuit.x(data[i])
    return circuit


def steane_apply_Z_logical(circuit, data):
    for i in range(7):
        circuit.z(data[i])
    return circuit


def steane_apply_H_logical(circuit, data):
    for i in range(7):
        circuit.h(data[i])
    return circuit


def steane_apply_S_logical(circuit, data):
    for i in range(7):
        circuit.s(data[i])
    return circuit


def steane_encoding(circuit, data):

    circuit.h(data[4])
    circuit.h(data[5])
    circuit.h(data[6])

    circuit.cx(data[0], data[1])
    circuit.cx(data[0], data[2])

    circuit.cx(data[6], data[0])
    circuit.cx(data[6], data[1])
    circuit.cx(data[6], data[3])

    
    circuit.cx(data[5], data[0])
    circuit.cx(data[5], data[2])
    circuit.cx(data[5], data[3])

    
    circuit.cx(data[4], data[1])
    circuit.cx(data[4], data[2])
    circuit.cx(data[4], data[3])


    circuit.barrier()

    return circuit

def steane_stabilizers_x(circuit, data, ancilla, stabilizers_indices):
    for i, indices in enumerate(stabilizers_indices):
        for qubit_index in indices:
            circuit.cx(data[qubit_index], ancilla[i])
        circuit.barrier()
    return circuit

def steane_stabilizers_z(circuit, data, ancilla, stabilizers_indices):
    for i, indices in enumerate(stabilizers_indices):
        circuit.h(ancilla[i])
        for qubit_index in indices:
            circuit.cx(ancilla[i], data[qubit_index])
        circuit.h(ancilla[i])
        circuit.barrier()    
    return circuit

# need to modify this for 2 kinds of ancillas one for the X ones for the Z
def steane_decoding(circuit, data, ancilla_x, ancilla_z, stabilizers_indices):

    circuit = steane_stabilizers_x(circuit, data, ancilla_x, stabilizers_indices)
    
    circuit = steane_stabilizers_z(circuit, data, ancilla_z, stabilizers_indices)
    
    return circuit


def steane_fix_x_error(circuit, data, stabilizer_classical_x):
    """
        Added conditional x based on the results of assessing the x_stabilizers.
        Used binary notation as it is simpler to map it to the syndromes rather than numbers
        in the c_if.
    """
    circuit.x(data[0]).c_if(stabilizer_classical_x, 0b001)
    circuit.x(data[1]).c_if(stabilizer_classical_x, 0b010)
    circuit.x(data[2]).c_if(stabilizer_classical_x, 0b011)
    circuit.x(data[3]).c_if(stabilizer_classical_x, 0b100)
    circuit.x(data[4]).c_if(stabilizer_classical_x, 0b101)
    circuit.x(data[5]).c_if(stabilizer_classical_x, 0b110)
    circuit.x(data[6]).c_if(stabilizer_classical_x, 0b111)
    
    return circuit

def steane_fix_z_error(circuit, data, stabilizer_classical_z):
    """
        Added conditional z based on the results of assessing the z_stabilizers.
        Used binary notation as it is simpler to map it to the syndromes rather than numbers
        in the c_if.
    """
    circuit.z(data[0]).c_if(stabilizer_classical_z, 0b001)
    circuit.z(data[1]).c_if(stabilizer_classical_z, 0b010)
    circuit.z(data[2]).c_if(stabilizer_classical_z, 0b011)
    circuit.z(data[3]).c_if(stabilizer_classical_z, 0b100)
    circuit.z(data[4]).c_if(stabilizer_classical_z, 0b101)
    circuit.z(data[5]).c_if(stabilizer_classical_z, 0b110)
    circuit.z(data[6]).c_if(stabilizer_classical_z, 0b111)

    return circuit


def steane_correct_error(circuit, data, stabilizer_classical_x, stabilizer_classical_z):
    # correct the error ---------------- c_if helps you do an if on the value of the classical register !
    # circuit.x(qreg[2]).c_if(creg, 3) <--------------- this is how to do it
    # correct the error ---------------- c_if helps you do an if on the value of the classical register !

    circuit = steane_fix_x_error(circuit, data, stabilizer_classical_x)

    circuit = steane_fix_z_error(circuit, data, stabilizer_classical_z)

    circuit.barrier()
    
    return circuit

# https://stem.mitre.org/quantum/error-correction-codes/steane-ecc.html
def steane_code(errors =[], verbose=False):

    stabilizers_indices = [
        [0, 2, 4, 6],  # First stabilizer indices
        [1, 2, 5, 6],  # Second stabilizer indices
        [3, 4, 5, 6]   # Third stabilizer indices
    ]

    # Define quantum registers
    data = QuantumRegister(7, 'D')     
    ancilla_x = QuantumRegister(3, 'A_x')  
    ancilla_z = QuantumRegister(3, 'A_z')   
    stabilizer_classical_x = ClassicalRegister(3, 'stabilizer_x_c')  # For stabilizers
    stabilizer_classical_z = ClassicalRegister(3, 'stabilizer_z_c')  # For stabilizers
    logical_classical = ClassicalRegister(7, 'logical_c')        # For logical qubit

    # Create quantum circuit
    circuit = QuantumCircuit(data, ancilla_x, ancilla_z, stabilizer_classical_x, stabilizer_classical_z, logical_classical)

    # circuit.h(data[0]) # - initial state can be encoded in data[0]

    circuit = steane_encoding(circuit, data)    

    ######## Add error here #####
    circuit = steane_Noisy_Channel(circuit, errors)
    ##############

    # circuit for decoding
    circuit = steane_decoding(circuit, data, ancilla_x, ancilla_z, stabilizers_indices)

    # measure stabilizer results into classical registers
    circuit.measure(ancilla_x[:], stabilizer_classical_x[:])
    circuit.measure(ancilla_z[:], stabilizer_classical_z[:])

    circuit = steane_correct_error(circuit, data, stabilizer_classical_x, stabilizer_classical_z)

    # measure the result after the error was corrected
    circuit.measure(data[:], logical_classical[:])

    return circuit


def analyze_Steane_logical_state(counts):
    # Define the mapping of physical states to logical states
    logical_state_mapping = {
        frozenset(["0000000", "0011110", "0101101", "0110011", "1001011", "1010101", "1100110", "1111000"]): "0",  # Logical 0 state
        frozenset(["0000111", "0011001", "0101010", "0110100", "1001100", "1010010", "1100001", "1111111"]): "1"   # Logical 1 state
    }

    total_counts = sum(counts.values())
    logical_state_counts = {}
    error_count = 0

    observed_states = {}

    for state, count in counts.items():
        logical_bits = state[:7]   # First 7 bits (logical qubit state)
        z_stabilizers = state[8:11]  # Z stabilizers result (next 3 bits)
        x_stabilizers = state[12:15]  # X stabilizers result (last 3 bits)

        # Determine if an error was detected in stabilizer measurements
        if '1' in z_stabilizers or '1' in x_stabilizers:
            error_count += count

        # Count occurrences of logical bit patterns
        if logical_bits in observed_states:
            observed_states[logical_bits] += count
        else:
            observed_states[logical_bits] = count

    # Match observed states to logical states
    for logical_pair, logical_value in logical_state_mapping.items():
        observed_count = sum(observed_states.get(state, 0) for state in logical_pair)

        if observed_count > 0:
            logical_state_counts[logical_value] = logical_state_counts.get(logical_value, 0) + observed_count

    # Determine the most likely logical state based on counts
    if logical_state_counts:
        deduced_state = max(logical_state_counts, key=logical_state_counts.get)
    else:
        deduced_state = "unknown"

    return {
        'deduced_state': deduced_state,
        'error_count': error_count,
        'total_occurrences': total_counts,
        'detailed_counts': logical_state_counts
    }


def pretty_print_Steane_results(results):
    print(f"Deduced logical state: {results['deduced_state']}")
    print(f"Error count: {results['error_count']}")
    print(f"Total occurrences: {results['total_occurrences']}")
    print(f"Detailed counts: {results['detailed_counts']}")
    print("")


def steane_Noisy_Channel(circuit, errors):
    # target_qubits = [0]
    # error_probs = {"x": 0.99 } # error_probs = {"x": 0.10, "z": 0.15, "y": 0.05}
    
    if not errors or not errors.get("target_qubits") or not errors.get("error_probs"):
        return circuit
    
    target_qubits = errors["target_qubits"]
    error_probs = errors["error_probs"]

    circuit = apply_errors_probabilistic(circuit, target_qubits, error_probs)
    return circuit