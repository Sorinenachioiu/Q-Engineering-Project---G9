from surface_codes.four_two_two import *
from qiskit import transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Estimator, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.quantum_info import Pauli, SparsePauliOp
from run_ibm.four_two_two.Deutsch import *

def run_422_on_ibm(backend):

    circuit = four_two_two_Deutsch_f11_constant()  
    
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(circuit)

    sampler = Sampler(mode=backend)
    
    job = sampler.run([isa_circuit])
    
    result = job.result()
    # Get results for the first (and only) PUB
    pub_result = result[0]
    
    # Get counts from the classical register "meas".
    print(f" >> Meas output register counts: {pub_result.data.meas.get_counts()}")
    
# order of running them was :
# 1. 00
# 2. 11 