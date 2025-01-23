from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from .errors import *


def shor_encoding(circuit, q):
    circuit.cx(q[0],q[3])
    circuit.cx(q[0],q[6])

    circuit.h(q[0])
    circuit.h(q[3])
    circuit.h(q[6])

    circuit.cx(q[0],q[1])
    circuit.cx(q[3],q[4])
    circuit.cx(q[6],q[7])

    circuit.cx(q[0],q[2])
    circuit.cx(q[3],q[5])
    circuit.cx(q[6],q[8])
    return circuit


def shor_noisy_channel(circuit, errors):
    # target_qubits = [0]
    # error_probs = {"x": 0.99 } # error_probs = {"x": 0.10, "z": 0.15, "y": 0.05}
    
    target_qubits = errors["target_qubits"]
    error_probs = errors["error_probs"]

    circuit = apply_errors_probabilistic(circuit, target_qubits, error_probs)
    return circuit


def shor_decoding_implicit_stabilizers(circuit, q):
    circuit.cx(q[0],q[1])
    circuit.cx(q[3],q[4])
    circuit.cx(q[6],q[7])

    circuit.cx(q[0],q[2])
    circuit.cx(q[3],q[5])
    circuit.cx(q[6],q[8])

    circuit.ccx(q[1],q[2],q[0])
    circuit.ccx(q[4],q[5],q[3])
    circuit.ccx(q[8],q[7],q[6])

    circuit.h(q[0])
    circuit.h(q[3])
    circuit.h(q[6])

    circuit.cx(q[0],q[3])
    circuit.cx(q[0],q[6])
    circuit.ccx(q[6],q[3],q[0])

    circuit.barrier(q)
    return circuit

# Stabilizer table from https://errorcorrectionzoo.org/c/shor_nine
# def shor_x_stabilizers():

#     x_stabilizers_indices = [
#         [0, 1, 2, 3, 4, 5],
#         [3, 4, 5, 6, 7, 8], 
#     ]

    


# def shor_z_stabilizers():
    
#     z_stabilizers_indices = [
#         [0, 1],
#         [1, 2],
#         [3, 4],
#         [4, 5],
#         [6, 7],
#         [7, 8],  
#     ]


def shor_code(errors, verbose=False):
    q = QuantumRegister(9,'q')
    c = ClassicalRegister(1,'c')

    circuit = QuantumCircuit(q, c)

    circuit = shor_encoding(q)

    ####error here############
    circuit = shor_noisy_channel(circuit, errors)
    ############################

    circuit = shor_decoding_implicit_stabilizers(circuit, q)

    circuit.measure(q[0],c[0])

    return circuit

