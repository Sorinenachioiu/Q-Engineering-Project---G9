from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from error_correction.errors import *
import math

def logical_X_first_q_422(circuit, data):
    circuit.barrier()

    circuit.x(data[0])
    circuit.x(data[2])

    circuit.barrier()
    return circuit


def logical_X_second_q_422(circuit, data):
    circuit.barrier()

    circuit.x(data[0])
    circuit.x(data[1])

    circuit.barrier()
    return circuit


def logical_Z_first_q_422(circuit, data):
    circuit.barrier()

    circuit.z(data[0])
    circuit.z(data[1])

    circuit.barrier()
    return circuit


def logical_Z_second_q_422(circuit, data):
    circuit.barrier()

    circuit.z(data[0])
    circuit.z(data[2])

    circuit.barrier()
    return circuit

# since it performs a swap operations be careful that the qubits are now inverted
def logical_SWAP_01_H_both_422(circuit, data):
    circuit.barrier()

    circuit.h(data[0])
    circuit.h(data[1])
    circuit.h(data[2])
    circuit.h(data[3])
    
    circuit.barrier()
    return circuit


def logical_CNOT_01_422(circuit, data):
    circuit.barrier()
    
    circuit.swap(0, 1)

    circuit.barrier()
    return circuit


def logical_CNOT_10_422(circuit, data):
    circuit.barrier()
    
    circuit.swap(0, 2)

    circuit.barrier()
    return circuit


def four_two_two_encoding_custom_states(circuit, data):

    circuit.cx(data[0], data[2])
    circuit.cx(data[1], data[2])
    circuit.h(data[3])

    circuit.cx(data[3], data[2])
    circuit.cx(data[3], data[1])
    circuit.cx(data[3], data[0])

    circuit.barrier()

    return circuit


def four_two_two_encoding(circuit, data):

    circuit.h(data[0])

    
    circuit.cx(data[0], data[1])
    circuit.cx(data[0], data[2])
    circuit.cx(data[0], data[3])

    circuit.barrier()

    return circuit


def four_two_two_decoding(circuit, data, ancilla, stabilizers_indices):

    for i, indices in enumerate(stabilizers_indices):
        for qubit_index in indices:
            circuit.cx(data[qubit_index], ancilla[i])
        circuit.barrier()
    
    for i, indices in enumerate(stabilizers_indices):
        circuit.h(ancilla[i+1])
        for qubit_index in indices:
            circuit.cx(ancilla[i+1], data[qubit_index])
        circuit.h(ancilla[i+1])
        circuit.barrier()    

    return circuit


def four_two_two_Noisy_Channel(circuit, errors):
    # target_qubits = [0]
    # error_probs = {"x": 0.99 } # error_probs = {"x": 0.10, "z": 0.15, "y": 0.05}
    
    if not errors or not errors.get("target_qubits") or not errors.get("error_probs"):
        return circuit
    
    target_qubits = errors["target_qubits"]
    error_probs = errors["error_probs"]

    circuit = apply_errors_probabilistic(circuit, target_qubits, error_probs)
    return circuit


def four_two_two_circuit_setup():
    stabilizers_indices = [
        [0, 1, 2, 3],  
    ]

    # Define quantum registers
    data = QuantumRegister(4, 'D')     
    ancilla = QuantumRegister(2, 'A')   
    stabilizer_classical = ClassicalRegister(2, 'stabilizer_c')  # For stabilizers
    logical_classical = ClassicalRegister(4, 'logical_c')        # For logical qubit

    # Create quantum circuit
    circuit = QuantumCircuit(data, ancilla, stabilizer_classical, logical_classical)
    
    return circuit, data, ancilla, stabilizer_classical, logical_classical, stabilizers_indices

# https://github.com/CSCfi/Quantum/blob/main/Grover-Search-on-Helmi/Grover_Search_error_detecting.ipynb
# https://errorcorrectionzoo.org/c/stab_4_2_2#citation-1
def four_two_two_code(initial_state = "00", errors = [], verbose=False):
    """
        initial state = the initial state of the two qubits, a string that belongs to ["00", "01", "10", "11"]
    """

    circuit, data, ancilla, stabilizer_classical, logical_classical, stabilizers_indices = four_two_two_circuit_setup()

    circuit = four_two_two_encoding(circuit, data)    

    circuit = four_two_two_initialize(circuit, data, initial_state)

    ### Add error here
    circuit = four_two_two_Noisy_Channel(circuit, errors)
    ###

    circuit = four_two_two_decoding(circuit, data, ancilla, stabilizers_indices)
    
    # circuit
    circuit.measure(ancilla[:], stabilizer_classical[:])

    circuit.measure(data[:], logical_classical[:])

    return circuit


def four_two_two_initialize(circuit, data, initial_state):
    # Initialize the system to the specified logical state (if provided)

    if initial_state == "00":
        pass  # |00> is the default state
    elif initial_state == "01":
        circuit.x(data[2])  
        circuit.x(data[3])
        circuit.barrier()
    elif initial_state == "10":
        circuit.x(data[1])
        circuit.x(data[3])
        circuit.barrier()  
    elif initial_state == "11":
        circuit.x(data[1])  
        circuit.x(data[2])  
        circuit.barrier()
    return circuit
    

def analyze_four_two_two_logical_state(counts):
    # Define the mapping of physical states to logical states
    logical_state_mapping = {
        frozenset(["0000", "1111"]): "00",  
        frozenset(["0011", "1100"]): "01",  
        frozenset(["0101", "1010"]): "10",  
        frozenset(["0110", "1001"]): "11",  
    }

    total_counts = sum(counts.values())

    logical_state_counts = {}
    error_count = 0

    observed_states = {}
    for state, count in counts.items():
        logical_bits = state[:4]  # Extract the first four bits (logical qubits)
        error_bits = state[5:]    # Extract last two bits (ancilla/stabilizer bits)

        # Determine if an error was detected based on stabilizer bits
        if '1' in error_bits:
            error_count += count
            continue

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

def pretty_print_four_two_two_results(results):
    print(f"Deduced logical state: {results['deduced_state']}")
    print(f"Error count: {results['error_count']}")
    print(f"Total occurrences: {results['total_occurrences']}")
    print(f"Detailed counts: {results['detailed_counts']}")
    print("")

    