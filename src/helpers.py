from matplotlib import pyplot as plt
from qiskit import QuantumCircuit
import os

def perform_experiment(backend, circuit, experiment_name, shots = 1024):
    try:
        print(f"\nCircuit diagram of {experiment_name} looks like:\n")
        print(circuit.draw(output='text'))
    except Exception as e:
        print((f"Error while drawing in the terminal the circuit: {e}"))

    if experiment_name is not None:
        save_circuit_png(circuit, experiment_name)

    # Execute the circuit on the backend
    try:
        job = backend.run(circuit, shots=shots)
        result = job.result()
        counts = result.get_counts(circuit)
        
        if experiment_name is not None:
            save_histogram(counts, experiment_name)

        print("Resulting counts:", counts)
        print("\n ----------------------------------------- ")
    except Exception as e:
        print(f"Error while executing the circuit: {e}")


def save_circuit_png(circuit, experiment_name):
    output_path = f'/app/output/{experiment_name}/circuit'
    directory = os.path.dirname(output_path)
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create directories as needed

    # Save the circuit diagram as a PNG
    fig = circuit.draw(output='mpl')
    fig.savefig(f'{output_path}.png')  
    print(f"Circuit diagram saved to {output_path}.png \n")


def save_histogram(counts, experiment_name):
    # Normalize the counts to probabilities
    total_shots = sum(counts.values())
    probabilities = {state: count / total_shots for state, count in counts.items()}

    # Prepare data for plotting
    labels = list(probabilities.keys())
    values = list(probabilities.values())

    # Create the histogram
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color="blue", alpha=0.7)
    plt.xlabel("Measurement Outcomes")
    plt.ylabel("Probability")
    plt.ylim(0, 1.0)
    plt.title("Measurement Result Histogram")

    # Annotate probabilities on top of each bar
    for i, value in enumerate(values):
        plt.text(i, value + 0.01, f"{value:.3f}", ha='center')

    # Save the histogram as a PNG file
    output_path = f'/app/output/{experiment_name}/histogram.png'
    directory = os.path.dirname(output_path)
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create directories as needed

    plt.savefig(output_path)
    plt.close()

    print(f"Histogram saved to {output_path}\n")


