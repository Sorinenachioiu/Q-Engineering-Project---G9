from experiments.framework import *
from experiments.properties.four_two_two_properites import *



EXPERIMENT_PROPERTIES = {
    "x_422": x_flip_0_015_properites_422,
    "y_422": y_flip_0_015_properites_422,
    "z_422": z_flip_0_015_properites_422
}

def run_experiments(backend, experiments_to_run):
    for experiment_key in experiments_to_run:
        
        if experiment_key in EXPERIMENT_PROPERTIES:
            experiment_properties = EXPERIMENT_PROPERTIES[experiment_key]()

            print(f"\nRunning experiment: {experiment_properties['experiment_path']}")

            qecc_experiment(backend, experiment_properties)

            print(f"\nDone with experiment: {experiment_properties['experiment_path']}")
        else:
            print(f"Experiment {experiment_key} not found in EXPERIMENT_PROPERTIES")