from matplotlib import pyplot as plt
from qiskit import QuantumCircuit
import os

def perform_experiment(backend, circuit, experiment_name, store_results = True, shots = 1024, verbose = True):
    try:
        if verbose:
            print(f"\nCircuit diagram of {experiment_name} looks like:\n")
            print(circuit.draw(output='text'))
    except Exception as e:
        print((f"Error while drawing in the terminal the circuit: {e}"))

    if store_results:
        save_circuit_png(circuit, experiment_name)
        save_circuit_latex(circuit, experiment_name)

    # Execute the circuit on the backend
    try:
        job = backend.run(circuit, shots=shots)
        result = job.result()
        counts = result.get_counts(circuit)
        
        if store_results:
            save_histogram(counts, experiment_name)

        if verbose:
            print("Resulting counts:", counts)
            print("\n ----------------------------------------- ")

        # fidelity = get_fidelity()

        return counts
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


def save_circuit_latex(circuit, experiment_name):
    output_path = f'/app/output/{experiment_name}/circuit'
    directory = os.path.dirname(output_path)
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create directories as needed

    # Save the circuit diagram as LaTeX
    with open(f'{output_path}.tex', 'w') as latex_file:
        latex_code = circuit.draw(output='latex_source')
        latex_file.write(latex_code)
    print(f"LaTeX circuit diagram saved to {output_path}.tex\n")


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


def save_experiment_plot(error_probabilities, success_rates, cont_probs, th_success_rates, 
                         physical_success_rates, experiment_name, experiment_path):
    
    output_path = f'/app/output/{experiment_path}/performance_plot'
    directory = os.path.dirname(output_path)

    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create the plot
    plt.figure(figsize=(8, 6))

    # Plot experimental success rates (discrete points)
    plt.plot(error_probabilities, success_rates, 'o', label="Experimental Success Rate")

    # Plot smooth theoretical approximation (fine-grained line)
    plt.plot(cont_probs, th_success_rates, linestyle='--', label="Theoretical Prediction")

    # Plot smooth physical success rate (fine-grained line)
    plt.plot(cont_probs, physical_success_rates, linestyle='--', label="Physical Success Rate")

    # Add labels and legend
    plt.xlabel("Error Probability")
    plt.ylabel("Success Rate")
    plt.title(f"Performance of {experiment_name} Code")

    # Adjust y-axis to focus on the range between 0.8 and 1 - for Steane
    # plt.ylim(0.9, 1)

    plt.grid(True)
    plt.legend()

    # Save the plot as PNG
    plt.savefig(f'{output_path}.png')
    plt.close()  # Close the plot to free memory

    print(f"Experiment performance plot saved to {output_path}.png")