from four_two_two import *
from helpers import *

def four_two_two_experiment_exaxmple(backend):
    counts = perform_experiment(backend, four_two_two_code("00"), "surface/four_two_two/no_error")

    experiment_result = analyze_four_two_two_logical_state(counts)

    pretty_print_four_two_two_results(experiment_result)