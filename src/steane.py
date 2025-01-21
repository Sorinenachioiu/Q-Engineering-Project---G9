from qiskit import transpile
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

def run_steane_code(backend):
    """Run Steane algorithm

    :param backend: Service backend
    """
    q = QuantumRegister(7, "q")
    c = ClassicalRegister(6, "c")
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

    #set up ancilla qubits
    #how to set them to 0?

    # set up bit flip detection
    qc.cnot(q[0], c[0])
    qc.cnot(q[2], c[0])
    qc.cnot(q[4], c[0])
    qc.cnot(q[6], c[0])

    qc.cnot(q[1], c[1])
    qc.cnot(q[2], c[1])
    qc.cnot(q[5], c[1])
    qc.cnot(q[6], c[1])

    qc.cnot(q[3], c[2])
    qc.cnot(q[4], c[2])
    qc.cnot(q[5], c[2])
    qc.cnot(q[6], c[2])

    # set up phase flip detection
    qc.h(c[3])
    qc.h(c[4])
    qc.h(c[5])

    qc.cnot(c[3], q[0])
    qc.cnot(c[3], q[2])
    qc.cnot(c[3], q[4])
    qc.cnot(c[3], q[6])

    qc.cnot(c[4], q[1])
    qc.cnot(c[4], q[2])
    qc.cnot(c[4], q[5])
    qc.cnot(c[4], q[6])

    qc.cnot(c[5], q[3])
    qc.cnot(c[5], q[4])
    qc.cnot(c[5], q[5])
    qc.cnot(c[5], q[6])

    qc.h(c[3])
    qc.h(c[4])
    qc.h(c[5])

    # measure final bits
    bit2 = qc.measure(c[0])
    bit1 = qc.measure(c[1])
    bit0 = qc.measure(c[2])

    phase2 = qc.measure(c[3])
    phase1 = qc.measure(c[4])
    phase0 = qc.meausure(c[5])

    # interpret measurements to find broken qubits
    # the bits are a 
    # binary encoding of number of quibit that has the respective error

    # run circuit??
    qc = transpile(qc, backend = backend)
    job = backend.run(qc, shots = 1)
    result = job.result()

    # print results
    print(result.get_counts(qc))
    return result
    