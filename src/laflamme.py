from qiskit import transpile
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit


def generate_laflamme_basis():
    """Generate circuit basis for Laflamme's correction code.
    q_logical[0] is the input state.

    :return: Circuit basis for Laflamme's correction code
    """

    q_logical = QuantumRegister(5, "q_logical")
    q_ancilla = QuantumRegister(4, "q_ancilla")
    c_logical = ClassicalRegister(5, "c_logical")
    c_ancilla = ClassicalRegister(4, "c_ancilla")
    qc = QuantumCircuit(q_logical, q_ancilla, c_logical, c_ancilla, name="Quantum Phase Estimation")

    return qc


def laflamme_encoding(qc):
    """Encode input state in the Laflamme's circuit.

    :param qc: Laflamme's circuit
    :return: Circuit with encoded input state
    """

    q_logical = qc.qregs[0]

    qc.z(q_logical[0])
    for x in range(5):
        qc.h(q_logical[x])

    for x in range(4):
        qc.cz(q_logical[0], q_logical[x + 1])

    qc.h(q_logical[0])
    qc.cz(q_logical[2], q_logical[3])
    qc.cz(q_logical[0], q_logical[1])
    qc.cz(q_logical[3], q_logical[4])
    qc.cz(q_logical[1], q_logical[2])
    qc.cz(q_logical[0], q_logical[4])

    return qc


def laflamme_correction(qc):
    """Correct the encoded state in the Laflamme's circuit.

    :param qc: Laflamme's circuit
    :return: Circuit with corrected encoded input state
    """

    q_logical = qc.qregs[0]
    q_ancilla = qc.qregs[1]
    c_logical = qc.cregs[0]
    c_ancilla = qc.cregs[1]

    for x in range(4):
        qc.h(q_ancilla[x])

    qc.cx(q_ancilla[0], q_logical[0])
    qc.cz(q_ancilla[0], q_logical[1])
    qc.cz(q_ancilla[0], q_logical[2])
    qc.cx(q_ancilla[0], q_logical[3])

    qc.cx(q_ancilla[1], q_logical[1])
    qc.cz(q_ancilla[1], q_logical[2])
    qc.cz(q_ancilla[1], q_logical[3])
    qc.cx(q_ancilla[1], q_logical[4])

    qc.cx(q_ancilla[2], q_logical[0])
    qc.cx(q_ancilla[2], q_logical[2])
    qc.cz(q_ancilla[2], q_logical[3])
    qc.cz(q_ancilla[2], q_logical[4])

    qc.cz(q_ancilla[3], q_logical[0])
    qc.cx(q_ancilla[3], q_logical[1])
    qc.cx(q_ancilla[3], q_logical[3])
    qc.cz(q_ancilla[3], q_logical[4])

    for x in range(4):
        qc.h(q_ancilla[x])

    for x in range(4):
        qc.measure(q_ancilla[x], c_ancilla[x])

    qc.x(q_logical[0]).c_if(c_ancilla, 0b1000)
    qc.x(q_logical[1]).c_if(c_ancilla, 0b0001)
    qc.x(q_logical[2]).c_if(c_ancilla, 0b0011)
    qc.x(q_logical[3]).c_if(c_ancilla, 0b0110)
    qc.x(q_logical[4]).c_if(c_ancilla, 0b1100)

    qc.z(q_logical[0]).c_if(c_ancilla, 0b0101)
    qc.z(q_logical[1]).c_if(c_ancilla, 0b1010)
    qc.z(q_logical[2]).c_if(c_ancilla, 0b0100)
    qc.z(q_logical[3]).c_if(c_ancilla, 0b1001)
    qc.z(q_logical[4]).c_if(c_ancilla, 0b0010)

    qc.y(q_logical[0]).c_if(c_ancilla, 0b1101)
    qc.y(q_logical[1]).c_if(c_ancilla, 0b1011)
    qc.y(q_logical[2]).c_if(c_ancilla, 0b0111)
    qc.y(q_logical[3]).c_if(c_ancilla, 0b1111)
    qc.y(q_logical[4]).c_if(c_ancilla, 0b1110)

    for x in range(5):
        qc.measure(q_logical[x], c_logical[x])

    return qc

def laflamme_decoding(qc):
    """Decode input state in the Laflamme's circuit.

        :param qc: Laflamme's circuit
        :return: Circuit with decoded input state
        """

    q_logical = qc.qregs[0]

    qc.cz(q_logical[0], q_logical[4])
    qc.cz(q_logical[1], q_logical[2])
    qc.cz(q_logical[3], q_logical[4])
    qc.cz(q_logical[0], q_logical[1])
    qc.cz(q_logical[2], q_logical[3])

    qc.h(q_logical[0])

    for x in range(4):
        qc.cz(q_logical[0], q_logical[4 - x])

    for x in range(5):
        qc.h(q_logical[4 - x])

    qc.z(q_logical[0])

    return qc

def generate_laflamme_circuit():
    """Generate Laflamme's correction code circuit

    :return: Laflamme's correction code circuit
    """

    return laflamme_correction(
        laflamme_encoding(
            generate_laflamme_basis()
        )
    )


def show_laflamme_circuit():
    """Display Laflamme's correction code circuit

    """

    print(
        generate_laflamme_circuit().draw(output = "text")
    )


def run_laflamme(backend, state):
    """Run Laflamme's correction code circuit

    :param backend: Service backend
    :param state: Input state to the circuit - False for 0 and True for 1
    :return: Result of the experiment
    """

    qc_basis = generate_laflamme_basis()
    if state:
        qc_basis.x(qc_basis.qregs[0][0])

    qc_encoded = laflamme_encoding(qc_basis)
    q_logical = qc_encoded.qregs[0]
    # qc_encoded.z(q_logical[2])

    qc = laflamme_correction(qc_encoded)

    qc_transpile = transpile(qc, backend=backend)
    job = backend.run(qc_transpile, shots=128)
    result = job.result()

    return map(lambda x: x[5:], list(result.get_counts(qc_transpile).keys()))
