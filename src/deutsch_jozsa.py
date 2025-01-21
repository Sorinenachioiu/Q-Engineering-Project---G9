from qiskit import transpile
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit


def run_deutsch_jozsa(backend):
    """Run Deutsch-Jozsa algorithm

    :param backend: Service backend
    """
    q = QuantumRegister(2, "q")
    c = ClassicalRegister(1, "c")
    qc = QuantumCircuit(q, c, name = "Deutsch-Jozsa")

    qc.x(q[1])

    qc.h(q[0])
    qc.h(q[1])

    qc.h(q[0])

    qc.measure(q[0], c)

    qc = transpile(qc, backend = backend)
    job = backend.run(qc, shots = 1)
    result = job.result()

    print(result.get_counts(qc))