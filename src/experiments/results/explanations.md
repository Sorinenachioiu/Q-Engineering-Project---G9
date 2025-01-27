# Experiments to run and their results

## Running experiments:
In the `properties` folder you can define define the properties of the experiment to be run and then add it to a list inside the `experiments.py` and run it from main.
By calling the `run_experiments` function inside of run_experiments.py

This will call `qecc_experiment` function from framework.py which will automatically run the experiments
with the given properites.


# Experiments methodology - How do we run the experiments?

## Theoretical computation of the success rate of the code

First, we establish a theoretical curve that represents the success rate of the code as a function of the error probability.

![mathematical expectations](assets/theoretical_way_of_computing.png)

Brief explanation:
- `errornum` - number of errors that we can encounter == number of qubits in the code
- `maxerrors` - maximum number of errors that can be corrected => we can get to the correct even though they appear
- `g(x) = 1-x` - probability of error in physical qubit
- `h(x)` - computes all the possible ways in which we can get `maxerrors` errors in `errornum` qubits and then correct them, getting the right result

\
![alt text](assets/theoretical_curve.png)

This is one such curve. What it means ?
- The `x-axis` represents the error probability. 
- The `y-axis` represents the success rate of the code.
- The `blue line` is the theoretical curve that we compute using the formula above.
- The `red line` is the success rate of a physical qubit. (1 - error probability, since we have no correction)
- `Interesction point` is the point at which a logical qubit encoded using the code performs the same as a physical qubit.


Therefore, with this theoretical value we know what we should expect from our simulation/ what pattern we should observe in the results.

## Assumptions made about errors:

- We only consider `errors` belonging to the `Pauli group. (X, Y, Z)`
- We only consider errors within a `Noisy Channel`, that is situated `between the encoding and decoding` of any code.
As that is the place where, in theory, most operations would be made during an actual algorithm.
- We consider the `error probability` to be the `same for all qubits`.
- We consider the `error probability` to be the `same for all types of errors.` (X, Y, Z)
- We consider that `any qubit can suffer from at most one error.`

## Experiment methodology:

For each experiment that we'll run we define the following properties:

![experiment properites](assets/experiment_properties.png)

- `experiment_type` - the `code` that `we want to test`
- `base_errors` - initial assumptions about errors
    - `target_qubits` - the qubits that can be affected by errors
    - `error_probability` - the probability of an error occuring for each type of error
- `runs_count` - the number of time we create the circuit and run it (*extra explanation below)
- `error_types` - specifies what types of errors we want to modify during the experiment
- `error_range` - the range of error probabilities that we want to test
- `number_of_samples` - the amount of equally spaced points in the `error_range` that define the error probabilities that we want to test. (e.g range = (0, 0.1), number_of_samples = 3 => we take three points 0, 0.05, 0.1 and run experiments for each of them)
- `shots` - amount of times we repeat an experiment with the same circuit
- `expected_state` - the state that we expect to get as result
- `experiment_path` - where we want to save the results of the experiment 


\
**Explanation of `runs_count`**:

- We want to `generate the circuit multiple times with a certain error probability` (as each time it is generated it can get different types of errors within the `Noisy channel`) and then run it multiple times to get a more accurate result. Thus geting a `meaningful average of the success rate of the code for that error probability.` 

Once this properites are defined, we can run the experiments automatically. Below is the code that runs one such experiment given the properites defined above (some parts are omitted for brevity).

```python
def qecc_experiment(backend, experiment_properties):

    ##### unpacking experiment_properites - prologue #####
    
    # take number_of_samples equally spaced values from the error_range interval 
    error_probabilities = np.linspace(error_range[0], error_range[1], number_of_samples)

    success_rates = []

    for error_probability in error_probabilities:
        current_errors = base_errors.copy()  # reset errors to base errors
        
        for error_type in error_types:
            if error_type in current_errors["error_probs"]:
                current_errors["error_probs"][error_type] = error_probability # update error probability for each type of error

        success_count = 0

        for i in range(runs_count):

            #### define experiment_name ####
            
            # run the experiment
            results = EXPERIMENT_TYPE[experiment_type](backend, experiment_type, experiment_name, current_errors, shots) 

            if results['deduced_state'] == expected_state:
                success_count += 1 

        success_rate = success_count / runs_count
        success_rates.append(success_rate)

        print(f"Error Probability: {error_probability:.2f}, Success Rate: {success_rate:.2%}")

    experiment_name = f"{experiment_type}"
    save_experiment_plot(error_probabilities, success_rates, experiment_name, experiment_path)
```

During the run of the experiment, the results of each individual experiment will be compared to the `expected_state` and the success rate of the code will be computed `for each error probability`. 

Then, the results will be plotted using matplotlib and saved in the `circuits/{experiment_path}` folder locally. 

The plot will contain the theoretical curve, the success rate of the physical qubit and the success rate of the code as a function of the error probability.

The framework defined for running the experiments is flexible and can be easily extended to run more experiments with different properties.


# [[4, 2, 2]] code 

Theoretical expectation of the success rate as a function of the error probability:

![theoretical - 422](assets/422_theoretical.png)

From this we can kind of infer that using it would make the error even more probable as the error rate increases. Thus, it is not a usable code.
Yet, from a theoretical perspective it is still interesting to investigate it. As the idea behind it is interesting. It encodes two qubits at the same time.
And it is one of the smallest codes that you can use. 

Let's see how it performs in practice by running some experiments. 

What we investigated is the following: 
- [x] How does the `success rate of the code` change as the error probability of `bit flips` increases?
![x - 422](assets/plots/four_two_two/performance_plot_x.png)

- [x] How does the `success rate of the code` change as the error probability of `phase flips` increases?
![z - 422](assets/plots/four_two_two/performance_plot_z.png)

- [x] How does the `success rate of the code` change as the error probability of `bit and phase flips` increases?
![y - 422](assets/plots/four_two_two/performance_plot_y.png)


As can be seen from the plots, the theoretical model is totaly accurate.







# Steane code  [[7, 1, 3]]

Theoretical expectation of the success rate as a function of the error probability:

![alt text](assets/steane_theoretical.png)

Compared to the [[4, 2, 2]] code, the Steane code can correct errors, thus it can for a really small erorr probability have a success rate grater than that of a physical qubit. Which is a desirable property of usable error correcting codes.

Yet, one impediment for the Steane code is that it is a bit more complex than the previous one. The circuit looks like this:


![alt text](assets/Steane_circuit.png)

Because it is this complex, one run takes a lot of time. And performing the whole experiment for a lot of error probabilities is a long process. Not only this, but another problem is that the range between it performs better than a physical qubit is somewhere around (0, 0.05). Meaning that the distance between the two curves, the one for the theoretical prediction and the one for the physical qubit is really small. Thus, it requires a lot of experiments to be run in order to make a meaningful plot that proves that in the simulation the Steane code really follows the theoretical prediction, being better than the physical qubit. As the differences of the curves is around ~0.01, which would mean that in 100 experiments we would have a difference of only 1 experiment... thus a really large number of experiments would need to be run. And because of the complexity of the circuit it would take a lot of time.

Below is the a warning that we get when running the Steane code, because of it's complexity:
![alt text](assets/warning_qinspire.png)

The experiments that we have run were again focused on x, y, z errors. And below are the properties that we used for the experiments:
![alt text](assets/properties_experiment_Steane.png)

So we run for each error probability 100 experiments. We needed to run this multiple times and we chronometered the time that it took to run the experiments, below is how much one such experiment takes: 

![alt text](assets/running_time_Steane.png)

7000 seconds... mean roughly somewhere around 2 hours to run. 
Yet, the results are not as satysfing as for [[4, 2, 2]]. 


What we investigated is the following: 
- [x] How does the `success rate of the code` change as the error probability of `bit flips` increases?
![x - 422](assets/plots/Steane/performance_plot_x.png)

- [x] How does the `success rate of the code` change as the error probability of `phase flips` increases?
![z - 422](assets/plots/Steane/performance_plot_z.png)

- [x] How does the `success rate of the code` change as the error probability of `bit and phase flips` increases?
![y - 422](assets/plots/Steane/performance_plot_y.png)


Thus, the Steane code seem to perform a little bit better than the physical qubit. Yet, the difference is not that big. And the theoretical prediction requires a really large amount to be proven in simulations. Stil.. this is proof that we can perform better than physical qubits. 


# Laflamme code [[5, 1, 3]]

Now, we want to investigate another code, which is the Laflamme code, which still encodes one qubit and has distance 3, yet it uses only 5 qubits, thus, there are less qubits that can be affected by errors. And the amount of errors that it can correct is still 1. Thus, in the theoretical prediciton we can see that it performs better than the physical qubit for a larger range of error probabilities than the Steane code. Thus, it means that not only does it matter to correct errors, but it is also important how many qubits we use. Thus this ratio between the number of qubits and the number of errors that we can correct is important. This can also be better understand by playing with the two params of the function that we use to compute the theoretical prediction. (https://www.geogebra.org/calculator/fj6st6hk - link to the function)

Meaning that we shouldn't only be considering the distance of the code, but also the number of qubits that we use. 

Theoretical expectation of the success rate as a function of the error probability:

![alt text](assets/laflamme_theoretical.png)

Laflamme was another code that had a pretty complex circuit, thus running the experiments for it was again a time consuming task.
![alt text](assets/running_time_laflamme.png)


What we investigated is the following: 
- [x] How does the `success rate of the code` change as the error probability of `bit flips` increases?
![x - laflamme](assets/plots/five_one_three/performance_plot_x.png)

- [x] How does the `success rate of the code` change as the error probability of `phase flips` increases?
![z - laflamme](assets/plots/five_one_three/performance_plot_z.png)

- [x] How does the `success rate of the code` change as the error probability of `bit and phase flips` increases?
![y - laflamme](assets/plots/five_one_three/performance_plot_y.png)



# Conclusion

We began with making a theoretical prediction of the success rate of the code as a function of the error probability. This was done by computing the probability of getting the right result by correcting the errors that we can encounter. 

Then, we ran experiments for the [[4, 2, 2]], Steane code [[7, 1, 3]] and Laflamme code [[5, 1, 3]].

We began with the [[4,2,2]] code, which was an interesting because it is based on the power of stabilizers. It does not perform better than a phyiscal qubit, yet it enables us to encode two qubits at the same time, while also allowing us to detect errors, thus, at the end of an experiment we would at least know that an error occured. 

Then, we moved to the Steane code ([[7,1,3]]), which is a bit more complex, yet it can correct errors, which let us understand how the recovery phase works in a QECC. The problem with it is that it is really complex and it takes a lot of time to run. And the range for which it outperforms the physical qubit is really small, yet it does outperform, meaning that by creating logical qubits we can get a better performance than by using regular ones. 

Lastly, we have worked with the Laflamme code ([[5,1,3]]), seeing that it outperforms the physical qubit for a larger range of error probabilities than the Steane code. This is because it uses less qubits, thus it is less error-prone. So, it means that there are two categories in which improvement can be made: how many qubits we use and how many errors we can correct.

Thus, people began to find scalable codes that can be implemented on real circuits, with varying connectivites. One such code is the surface code, which is a 2D code that can be implemented on a 2D grid of qubits. This code is scalable and can be implemented on real quantum computers that are built using superconducting qubits, because they only support well nearest neighbors connectivities. see more in: [surface codes](/src/surface_codes/documentation/documentation.md)
