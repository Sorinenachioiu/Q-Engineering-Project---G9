from experiments.framework import *
from experiments.properties.four_two_two_properites import *
from experiments.properties.steane_properties import *
from experiments.properties.laflamme_properites import *


EXPERIMENT_PROPERTIES = {
    ## [[4, 2, 2]] code
    "x_422": x_flip_0_025_properites_422,
    "y_422": y_flip_0_025_properites_422,
    "z_422": z_flip_0_025_properites_422,
    
    ## Steane code ([[7, 1, 3]])
    "x_Steane": x_flip_0_005_properites_steane,
    "y_Steane": y_flip_0_005_properites_steane,
    "z_Steane": z_flip_0_005_properites_steane,

    ## Laflamme code ([[5, 1, 3]])
    "x_513":  x_flip_0_014_properites_513,
    "y_513":  y_flip_0_014_properites_513,
    "z_513":  z_flip_0_014_properites_513,
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