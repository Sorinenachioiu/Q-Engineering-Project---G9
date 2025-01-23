from surface_codes.four_two_two import *
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

############### For Deutsch's algorithm on ibm quantum ###################
#
# f = const, when all outputs are 0, or all outputs are 1
# f = balanced, if half of the outputs are 0 and half are 1
#
# measurement output = 0 -> constant
# measurement output = 1 -> balanced

def prologue_four_two_two(initial_state):
    # Get the encoding of four two two, at the begining

    circuit, data, ancilla, stabilizer_classical, logical_classical, stabilizers_indices = four_two_two_circuit_setup()

    circuit = four_two_two_encoding(circuit, data)    

    circuit = four_two_two_initialize(circuit, data, initial_state)

    return circuit, data, ancilla, stabilizer_classical, logical_classical, stabilizers_indices


def epilogue_four_two_two(circuit, data, ancilla, stabilizer_classical, logical_classical, stabilizers_indices):
    # Apply stabilizers and measure at the end of the four two two

    # Apply stabilizers
    circuit = four_two_two_decoding(circuit, data, ancilla, stabilizers_indices)
    
    # measure results
    circuit.measure(ancilla[:], stabilizer_classical[:])

    circuit.measure(data[:], logical_classical[:])

    return circuit


def four_two_two_Deutsch_f00_constant():
    # Deutsch requires the two qubits in |0>|1>
    # Yet, we initialize in |1>|0> since the logical hadamard also swaps the qubits
    # so we look at the circuit as usual
    # Step 1: initialize
    circuit, data, ancilla, stabilizer_classical, logical_classical, stabilizers_indices = prologue_four_two_two("10") 

    # Step 2: Hadamard both qubits
    circuit = logical_SWAP_01_H_both_422(circuit, data)

    # Step 3: apply oracle
    # Since we have the f(x) = 0 function (constant), we don't apply anything

    # Step 4: Hadamard first qubit before measurement(yet, the logical operator forces us to hadamard both)
    # so the actual result will be in logical qubit 2, not 1 as usually
    circuit = logical_SWAP_01_H_both_422(circuit, data)

    # Step 5: Apply stabilizers and measure everything
    epilogue_four_two_two(circuit, data, ancilla, stabilizer_classical, logical_classical, stabilizers_indices)

    return circuit


def four_two_two_Deutsch_f11_constant():
    # Deutsch requires the two qubits in |0>|1>
    # Yet, we initialize in |1>|0> since the logical hadamard also swaps the qubits
    # so we look at the circuit as usual
    # Step 1: initialize
    circuit, data, ancilla, stabilizer_classical, logical_classical, stabilizers_indices = prologue_four_two_two("10") 
    
    # Step 2: Hadamard both qubits
    circuit = logical_SWAP_01_H_both_422(circuit, data)

    # Step 3: apply oracle
    # Since we have the f(x) = 1 function (constant), we apply an X flip on the second qubit
    circuit = logical_X_second_q_422(circuit, data)

    # Step 4: Hadamard first qubit before measurement(yet, the logical operator forces us to hadamard both)
    # so the actual result will be in logical qubit 2, not 1 as usually
    circuit = logical_SWAP_01_H_both_422(circuit, data)

    # Step 5: Apply stabilizers and measure everything
    epilogue_four_two_two(circuit, data, ancilla, stabilizer_classical, logical_classical, stabilizers_indices)

    return circuit


def four_two_two_Deutsch_f01_balanced():
    # Deutsch requires the two qubits in |0>|1>
    # Yet, we initialize in |1>|0> since the logical hadamard also swaps the qubits
    # so we look at the circuit as usual
    # Step 1: initialize
    circuit, data, ancilla, stabilizer_classical, logical_classical, stabilizers_indices = prologue_four_two_two("10")
    
    # Step 2: Hadamard both qubits
    circuit = logical_SWAP_01_H_both_422(circuit, data)
    
    # Step 3: apply oracle
    # Since we have the f(x) = x function (balanced), we apply CNOT01
    circuit = logical_CNOT_01_422(circuit, data)

    # Step 4: Hadamard first qubit before measurement(yet, the logical operator forces us to hadamard both)
    # so the actual result will be in logical qubit 2, not 1 as usually
    circuit = logical_SWAP_01_H_both_422(circuit, data)

    # Step 5: Apply stabilizers and measure everything
    epilogue_four_two_two(circuit, data, ancilla, stabilizer_classical, logical_classical, stabilizers_indices)

    return circuit


def four_two_two_Deutsch_f10_balanced():
    # Deutsch requires the two qubits in |0>|1>
    # Yet, we initialize in |1>|0> since the logical hadamard also swaps the qubits
    # so we look at the circuit as usual
    # Step 1: initialize
    circuit, data, ancilla, stabilizer_classical, logical_classical, stabilizers_indices = prologue_four_two_two("10")
    
    # Step 2: Hadamard both qubits
    circuit = logical_SWAP_01_H_both_422(circuit, data)


    # Step 3: apply oracle
    # Since we have the f(x) = (x + 1) mod 2  function, balanced we apply CNOT01 followed by X_2
    circuit = logical_CNOT_01_422(circuit, data)
    circuit = logical_X_second_q_422(circuit, data)


    # Step 4: Hadamard first qubit before measurement(yet, the logical operator forces us to hadamard both)
    # so the actual result will be in logical qubit 2, not 1 as usually
    circuit = logical_SWAP_01_H_both_422(circuit, data)

    # Step 5: Apply stabilizers and measure everything
    epilogue_four_two_two(circuit, data, ancilla, stabilizer_classical, logical_classical, stabilizers_indices)

    return circuit
