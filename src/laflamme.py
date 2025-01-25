from qiskit import transpile
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from error_correction.errors import *

def generate_laflamme_basis(state):
    """Generate circuit basis for Laflamme's correction code.
    q_logical[0] is the input state.

    :return: Circuit basis for Laflamme's correction code
    """

    q_logical = QuantumRegister(5, "q_logical")
    q_ancilla = QuantumRegister(4, "q_ancilla")
    c_logical = ClassicalRegister(5, "c_logical")
    c_ancilla = ClassicalRegister(4, "c_ancilla")
    qc = QuantumCircuit(q_logical, q_ancilla, c_logical, c_ancilla, name="Quantum Phase Estimation")

    if state:
        qc.x(qc.qregs[0][0])

    return qc


def laflamme_encoding(qc):
    """Encode input state in the Laflamme's circuit.

    :param qc: Laflamme's circuit
    :return: Circuit with encoded input state
    """

    q_logical = qc.qregs[0]

    qc.z(q_logical[0])
    for x in range(5):
        qc.h(q_logical[x])

    for x in range(4):
        qc.cz(q_logical[0], q_logical[x + 1])

    qc.h(q_logical[0])
    qc.cz(q_logical[2], q_logical[3])
    qc.cz(q_logical[0], q_logical[1])
    qc.cz(q_logical[3], q_logical[4])
    qc.cz(q_logical[1], q_logical[2])
    qc.cz(q_logical[0], q_logical[4])

    qc.barrier()

    return qc


def laflamme_correction(qc):
    """Correct the encoded state in the Laflamme's circuit.

    :param qc: Laflamme's circuit
    :return: Circuit with corrected encoded input state
    """

    q_logical = qc.qregs[0]
    q_ancilla = qc.qregs[1]
    c_logical = qc.cregs[0]
    c_ancilla = qc.cregs[1]

    for x in range(4):
        qc.h(q_ancilla[x])

    qc.barrier()

    qc.cx(q_ancilla[0], q_logical[0])
    qc.cz(q_ancilla[0], q_logical[1])
    qc.cz(q_ancilla[0], q_logical[2])
    qc.cx(q_ancilla[0], q_logical[3])
    qc.barrier()

    qc.cx(q_ancilla[1], q_logical[1])
    qc.cz(q_ancilla[1], q_logical[2])
    qc.cz(q_ancilla[1], q_logical[3])
    qc.cx(q_ancilla[1], q_logical[4])
    qc.barrier()

    qc.cx(q_ancilla[2], q_logical[0])
    qc.cx(q_ancilla[2], q_logical[2])
    qc.cz(q_ancilla[2], q_logical[3])
    qc.cz(q_ancilla[2], q_logical[4])
    qc.barrier()

    qc.cz(q_ancilla[3], q_logical[0])
    qc.cx(q_ancilla[3], q_logical[1])
    qc.cx(q_ancilla[3], q_logical[3])
    qc.cz(q_ancilla[3], q_logical[4])
    qc.barrier()

    for x in range(4):
        qc.h(q_ancilla[x])
    qc.barrier()

    for x in range(4):
        qc.measure(q_ancilla[x], c_ancilla[x])

    qc.x(q_logical[0]).c_if(c_ancilla, 0b1000)
    qc.x(q_logical[1]).c_if(c_ancilla, 0b0001)
    qc.x(q_logical[2]).c_if(c_ancilla, 0b0011)
    qc.x(q_logical[3]).c_if(c_ancilla, 0b0110)
    qc.x(q_logical[4]).c_if(c_ancilla, 0b1100)

    qc.z(q_logical[0]).c_if(c_ancilla, 0b0101)
    qc.z(q_logical[1]).c_if(c_ancilla, 0b1010)
    qc.z(q_logical[2]).c_if(c_ancilla, 0b0100)
    qc.z(q_logical[3]).c_if(c_ancilla, 0b1001)
    qc.z(q_logical[4]).c_if(c_ancilla, 0b0010)

    qc.y(q_logical[0]).c_if(c_ancilla, 0b1101)
    qc.y(q_logical[1]).c_if(c_ancilla, 0b1011)
    qc.y(q_logical[2]).c_if(c_ancilla, 0b0111)
    qc.y(q_logical[3]).c_if(c_ancilla, 0b1111)
    qc.y(q_logical[4]).c_if(c_ancilla, 0b1110)

    qc.barrier()

    for x in range(5):
        qc.measure(q_logical[x], c_logical[x])

    qc.barrier()

    return qc

def laflamme_decoding(qc):
    """Decode input state in the Laflamme's circuit.

        :param qc: Laflamme's circuit
        :return: Circuit with decoded input state
        """

    q_logical = qc.qregs[0]

    qc.cz(q_logical[0], q_logical[4])
    qc.cz(q_logical[1], q_logical[2])
    qc.cz(q_logical[3], q_logical[4])
    qc.cz(q_logical[0], q_logical[1])
    qc.cz(q_logical[2], q_logical[3])

    qc.h(q_logical[0])

    for x in range(4):
        qc.cz(q_logical[0], q_logical[4 - x])

    for x in range(5):
        qc.h(q_logical[4 - x])

    qc.z(q_logical[0])

    qc.barrier()

    return qc

def generate_laflamme_circuit(errors = [], init_state = False):
    """Generate Laflamme's correction code circuit

    :return: Laflamme's correction code circuit
    """

    return laflamme_correction(
        laflamme_Noisy_Channel(
            laflamme_encoding(
                generate_laflamme_basis(init_state)
            ), errors)
    )


def show_laflamme_circuit():
    """Display Laflamme's correction code circuit

    """

    print(
        generate_laflamme_circuit().draw(output = "text")
    )


def run_laflamme(backend, state):
    """Run Laflamme's correction code circuit

    :param backend: Service backend
    :param state: Input state to the circuit - False for 0 and True for 1
    :return: Result of the experiment
    """

    qc_basis = generate_laflamme_basis(state)

    qc_encoded = laflamme_encoding(qc_basis)
    q_logical = qc_encoded.qregs[0]
    # qc_encoded.z(q_logical[2])

    qc = laflamme_correction(qc_encoded)

    qc_transpile = transpile(qc, backend=backend)
    job = backend.run(qc_transpile, shots=128)
    result = job.result()

    return map(lambda x: x[5:], list(result.get_counts(qc_transpile).keys()))


### TODO FINISH BELOW

def analyze_laflamme_logical_state(counts):
    # Define the mapping of physical states to logical states
    logical_state_mapping = {
        frozenset(["00000", "00011", "00101", "00110", "01001", "01010", "01100", "01111", "10001", "10010", "10100", "10111", "11000", "11011", "11101", "11110"]): "0",  # Logical 0 state
        frozenset(["00001", "00010", "00100", "00111", "01000", "01011", "01101", "01110", "10000", "10011", "10101", "10110", "11001", "11010", "11100", "11111"]): "1"   # Logical 1 state
    }

    total_counts = sum(counts.values())
    logical_state_counts = {}
    error_count = 0

    observed_states = {}

    for state, count in counts.items():
        stabilizers_bits = state[:4]   # First 4 bits for stabilizers
        logical_bits = state[5:]  # 5 bits (logical qubit state)

        # Determine if an error was detected in stabilizer measurements
        if '1' in stabilizers_bits:
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


def pretty_print_laflamme_results(results):
    print(f"Deduced logical state: {results['deduced_state']}")
    print(f"Error count: {results['error_count']}")
    print(f"Total occurrences: {results['total_occurrences']}")
    print(f"Detailed counts: {results['detailed_counts']}")
    print("")


def laflamme_Noisy_Channel(circuit, errors):
    # target_qubits = [0]
    # error_probs = {"x": 0.99 } # error_probs = {"x": 0.10, "z": 0.15, "y": 0.05}
    
    if not errors or not errors.get("target_qubits") or not errors.get("error_probs"):
        return circuit
    
    target_qubits = errors["target_qubits"]
    error_probs = errors["error_probs"]

    circuit = apply_errors_probabilistic(circuit, target_qubits, error_probs)
    return circuit