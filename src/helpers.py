from matplotlib import pyplot as plt
from qiskit import QuantumCircuit

def save_circuit_png(circuit, file_name):
    fig = circuit.draw(output='mpl')
    fig.savefig(f'/app/output/{file_name}.png')  
    print(f"Circuit diagram saved to /app/output/{file_name}.png")