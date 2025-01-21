from qiskit import transpile
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

from math import pi


def generate_qphase_circuit(bit_precision):
    """Generate Quantum Phase Estimation circuit of specified bit precision

    :param bit_precision: Number of bits to which the phase is estimated
    :return: Quantum Phase Estimation circuit
    """
    q = QuantumRegister(bit_precision + 1, "q")
    c = ClassicalRegister(bit_precision, "c")
    qc = QuantumCircuit(q, c, name="Quantum Phase Estimation")

    # State preparation (eigenstate of Pauli X with eigenvalue -1)
    qc.x(q[bit_precision])
    qc.h(q[bit_precision])

    # Hadamard transform all qubits
    for x in range(bit_precision):
        qc.h(q[x])

    # Apply powers of chosen quantum gate (Pauli X)
    for x in range(bit_precision):
        for y in range(2 ** x):
            qc.cx(q[bit_precision - x - 1], q[bit_precision])

    # Swap first and last qubit, second and second-to-last and so on
    for x in range(bit_precision // 2):
        qc.swap(q[x], q[bit_precision - x - 1])

    # Apply Inverse QFT
    for x in range(bit_precision):
        qc.h(q[bit_precision - x - 1])
        for y in range(x):
            qc.crz(pi / 2 ** (y + 2), q[bit_precision - x + y], q[bit_precision - x - 1])

    # Measure qubits
    for x in range(bit_precision):
        qc.measure(q[x], c[x])

    return qc


def show_qphase_estimation_circuit(bit_precision):
    """Display Quantum Phase Estimation circuit of specified bit precision

    :param bit_precision: Number of bits to which the phase is estimated
    """
    print(
        generate_qphase_circuit(bit_precision).draw(output = "text")
    )


def run_qphase_estimation(backend, bit_precision):
    """Run Quantum Phase Estimation algorithm with specified bit precision

    :param backend: Service backend
    :param bit_precision: Number of bits to which the phase is estimated
    :return:
    """
    qc = transpile(generate_qphase_circuit(bit_precision), backend=backend)
    job = backend.run(qc, shots=1)
    result = job.result()

    return result.get_counts(qc)
