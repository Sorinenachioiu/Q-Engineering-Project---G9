from qiskit import transpile
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

#alright alright alright
def run_steane_code(backend):
    """Run Steane algorithm

    :param backend: Service backend
    """
    q = QuantumRegister(7, "q")
    c = ClassicalRegister(1, "c")
    qc = QuantumCircuit(q, c, name = "Steane")

    # create the encoding circuit
    qc.h(q[4])
    qc.h(q[5])
    qc.h(q[6])

    qc.cnot(q[0], q[1])
    qc.cnot(q[0], q[2])

    qc.cnot(q[6], q[0])
    qc.cnot(q[6], q[1])
    qc.cnot(q[6], q[3])

    qc.cnot(q[5], q[0])
    qc.cnot(q[5], q[2])
    qc.cnot(q[5], q[3])

    qc.cnot(q[4], q[1])
    qc.cnot(q[4], q[2])
    qc.cnot(q[4], q[3])

    #run circuit
    qc = transpile(qc, backend = backend)
    job = backend.run(qc, shots = 1)
    result = job.result()

    #print results
    print(result.get_counts(qc))
    