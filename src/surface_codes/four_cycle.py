from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from error_correction.errors import *

def four_cycle(errors = [], verbose=False):
    # Define quantum registers
    data = QuantumRegister(2, 'D')      # Data qubits (D1, D2)
    ancilla = QuantumRegister(2, 'A')   # Ancilla qubits (A1, A2)
    classical = ClassicalRegister(2, 'c')  # Classical bits for measurement

    # Create quantum circuit
    circuit = QuantumCircuit(data, ancilla, classical)

    # Apply stabilizer checks
    circuit.h(ancilla[0])       
    circuit.cx(data[0], ancilla[0])  
    circuit.cx(data[1], ancilla[0])  
    circuit.h(ancilla[0])       

    # Second ancilla qubit 
    circuit.h(ancilla[1])       
    circuit.cz(data[0], ancilla[1])  
    circuit.cz(data[1], ancilla[1])  
    circuit.h(ancilla[1])       

    # Measure ancilla qubits
    circuit.measure(ancilla, classical)

    return circuit
