from helpers import *
from run_ibm.four_two_two.Deutsch import *

def f00_run(backend):
    print ("Running f(x) = 0 to check if constant using logical qubits encoded using [[4, 2, 2]]")

    counts = perform_experiment(backend, four_two_two_Deutsch_f00_constant(), "422/Deutsch/00_const", shots=1024)

    results = analyze_four_two_two_logical_state(counts)

    pretty_print_four_two_two_results(results)
    
    print ("---------------------------------------------")


def f11_run(backend):
    print ("Running f(x) = 1 to check if constant using logical qubits encoded using [[4, 2, 2]]")

    counts = perform_experiment(backend, four_two_two_Deutsch_f11_constant(), "422/Deutsch/11_const", shots=1024)

    results = analyze_four_two_two_logical_state(counts)

    pretty_print_four_two_two_results(results)
    
    print ("---------------------------------------------")


def f01_run(backend):
    print ("Running f(x) = x to check if balanced using logical qubits encoded using [[4, 2, 2]]\n")

    counts = perform_experiment(backend, four_two_two_Deutsch_f01_balanced(), "422/Deutsch/01_balanced", shots=1024)

    results = analyze_four_two_two_logical_state(counts)

    pretty_print_four_two_two_results(results)

    print ("---------------------------------------------\n")


def f10_run(backend):
    print ("Running f(x) = (x+1) mod 2  to check if balanced using logical qubits encoded using [[4, 2, 2]]\n")
    
    counts = perform_experiment(backend, four_two_two_Deutsch_f10_balanced(), "422/Deutsch/10_balanced", shots=1024)

    results = analyze_four_two_two_logical_state(counts)

    pretty_print_four_two_two_results(results)


def run_Deutsch_logical_422_qi(backend):

    f00_run(backend)
    f11_run(backend)
    f01_run(backend)
    f10_run(backend)
    


