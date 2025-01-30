from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from .errors import *


def bit_flip_code(errors = [], verbose=False):
    # Create a quantum circuit with 2 qubits
    circuit = QuantumCircuit(2)

    q = QuantumRegister(3,'q')
    c = ClassicalRegister(1,'c')

    circuit = QuantumCircuit(q,c)

    circuit.cx(q[0],q[1])
    circuit.cx(q[0],q[2])

    ####error here############
    # circuit = apply_errors(circuit, errors)
    ############################

    # circuit.cx(q[0],q[1])
    # circuit.cx(q[0],q[2])
    # circuit.ccx(q[2],q[1],q[0])
    # circuit.measure(q[0],c[0])

    return circuit

def bit_flip_code_probabilistic_error(verbose=False):
    # Create a quantum circuit with 2 qubits
    circuit = QuantumCircuit(2)

    q = QuantumRegister(3,'q')
    c = ClassicalRegister(1,'c')

    circuit = QuantumCircuit(q,c)

    circuit.cx(q[0],q[1])
    circuit.cx(q[0],q[2])

    ####error here############
    target_qubits = [0, 1, 2]
    error_probs = {"x": 0.10, "z": 0.15, "y": 0.05}
    circuit = apply_errors_probabilistic(circuit, target_qubits, error_probs)
    ############################

    circuit.cx(q[0],q[1])
    circuit.cx(q[0],q[2])
    circuit.ccx(q[2],q[1],q[0])
    circuit.measure(q[0],c[0])

    return circuit


def phase_flip_code(errors = [], verbose=False):
    q = QuantumRegister(3,'q')
    c = ClassicalRegister(1,'c')

    circuit = QuantumCircuit(q,c)

    circuit.cx(q[0],q[1])
    circuit.cx(q[0],q[2])

    circuit.h(q[0])
    circuit.h(q[1])
    circuit.h(q[2]) 
    
    ####error here############
    # circuit = apply_errors(circuit, errors)
    ############################

    # circuit.h(q[0])
    # circuit.h(q[1])
    # circuit.h(q[2])

    # circuit.cx(q[0],q[1])
    # circuit.cx(q[0],q[2])
    # circuit.ccx(q[2],q[1],q[0])
    # circuit.measure(q[0],c[0])
    return circuit

