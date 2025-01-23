from qiskit import transpile
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit


def run_deutsch_jozsa(backend):
    """Run Deutsch-Jozsa algorithm with a balanced oracle.

    :param backend: Service backend
    """
    q = QuantumRegister(2, "q")  # Two qubits: one for input, one for output
    c = ClassicalRegister(1, "c")  # Single classical register to store results
    qc = QuantumCircuit(q, c, name="Deutsch-Jozsa")

    # Step 1: Initialization
    qc.x(q[1])  # Set the auxiliary qubit to |1>
    qc.h(q[0])
    qc.h(q[1])

    # Step 2: Balanced Oracle (CX gate to represent f(x) = x)
    qc.cx(q[0], q[1])  # Controlled-NOT acts as a balanced function

    # Step 3: Apply Hadamard again to the input qubit
    qc.h(q[0])

    # Step 4: Measure the input qubit
    qc.measure(q[0], c)

    return qc