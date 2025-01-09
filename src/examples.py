from qiskit import QuantumCircuit
from helpers import *

def universal_gate_set(backend, verbose=False):
    """
    Demonstrate a universal quantum gate set on the given backend.

    Args:
        backend: The Quantum Inspire backend to execute the circuit.
        verbose: If True, provides additional details about the execution process.
    """
    # Create a quantum circuit with 2 qubits
    circuit = QuantumCircuit(2)

    # Apply universal quantum gates
    circuit.h(0)      # Hadamard gate
    circuit.x(1)      # Pauli-X gate
    circuit.y(0)      # Pauli-Y gate
    circuit.z(1)      # Pauli-Z gate
    circuit.s(0)      # Phase (S) gate
    circuit.t(1)      # T gate
    circuit.cx(0, 1)  # Controlled-NOT gate

    # Measure all qubits
    circuit.measure_all()

    # Print the circuit
    print("Circuit for Universal Quantum Gate Set:")
    print(circuit.draw(output='text'))

    save_circuit_png(circuit, "universal_set")

    # Execute the circuit on the backend
    try:
        job = backend.run(circuit, shots=1024)
        result = job.result()
        counts = result.get_counts(circuit)
        print("Resulting counts:", counts)
    except Exception as e:
        print(f"Error while executing the universal gate set circuit: {e}")


def grovers_algorithm(backend, verbose=False):
    """
    Grover's Algorithm for searching decimal number 6 (binary |110>) in a database of size 2^3.

    Args:
        backend: The Quantum Inspire backend to execute the circuit.
        verbose: If True, provides additional details about the execution process.
    """
    # Number of qubits
    n_qubits = 3

    # Initialize the circuit
    circuit = QuantumCircuit(n_qubits)

    # Step 1: Initialize all qubits in superposition
    circuit.h(range(n_qubits))

    # Step 2: Apply Grover's operator (Oracle + Diffusion) twice
    for _ in range(2):
        # Oracle: Marking the state |110>
        circuit.x(0)  # Apply X to the first qubit
        circuit.h(2)  # Apply H to the last qubit (ancillary qubit)
        circuit.ccx(0, 1, 2)  # Toffoli gate marking |110>
        circuit.h(2)  # Apply H to the last qubit
        circuit.x(0)  # Undo X on the first qubit

        # Diffusion Operator
        circuit.h(range(n_qubits))  # Apply H to all qubits
        circuit.x(range(n_qubits))  # Apply X to all qubits
        circuit.h(2)  # Apply H to the last qubit
        circuit.ccx(0, 1, 2)  # Toffoli gate for inversion about the mean
        circuit.h(2)  # Apply H to the last qubit
        circuit.x(range(n_qubits))  # Undo X on all qubits
        circuit.h(range(n_qubits))  # Undo H on all qubits

    # Step 3: Measure all qubits
    circuit.measure_all()

    # Print the circuit
    print("Grover's Algorithm Circuit for Searching |110>:")
    print(circuit.draw(output='text'))

    # Save the circuit as a PNG file
    save_circuit_png(circuit, "grover_find_6")

    # Execute the circuit on the backend
    try:
        job = backend.run(circuit, shots=1024)
        result = job.result()
        counts = result.get_counts(circuit)
        print("Resulting counts:", counts)
    except Exception as e:
        print(f"Error while executing Grover's algorithm circuit: {e}")
