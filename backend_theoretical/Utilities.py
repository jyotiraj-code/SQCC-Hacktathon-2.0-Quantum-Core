from functools import partial
import numpy as np
from qiskit import Aer, transpile
from qiskit.providers.aer import QasmSimulator
from scipy.optimize import shgo
from . import KnapsackMethod
from . import Circuits
from qiskit import BasicAer

backend = Aer.get_backend("aer_simulator_statevector")
is_apply_noise = False

def get_statevector(transpiled_circuit, parameter_dict):
    bound_circuit = transpiled_circuit.bind_parameters(parameter_dict)
    if is_apply_noise:
        result = backend.run(bound_circuit, shots=1).result()
    else:
        result = backend.run(bound_circuit, shots=1).result()
    statevector = result.get_statevector()
    return statevector

def average_value(probs_dict, func):
    bitstrings = list(probs_dict.keys())
    values = np.array(list(map(func, bitstrings)))
    probs = np.array(list(probs_dict.values()))
    return sum(values * probs)

def optimize_angles(p, angles_to_value, gamma_range, beta_range):
    bounds = np.array([gamma_range, beta_range] * p)
    result = shgo(angles_to_value, bounds, iters=3)
    return result.x

def bitstring_to_choice(bitstring, problem):
    bits = np.array(list(map(int, list(bitstring))))[::-1]
    choice = np.array(bits[:problem.N])
    return choice

def objective_function(bitstring, problem):
    choice = bitstring_to_choice(bitstring, problem)
    value = choice.dot(problem.values)
    return value

def to_parameter_dict(angles, circuit):
    gammas = angles[0::2]
    betas = angles[1::2]
    parameters = {}
    for parameter, value in zip(circuit.betas, betas):
        parameters[parameter] = value
    for parameter, value in zip(circuit.gammas, gammas):
        parameters[parameter] = value
    return parameters

def get_probs_dict(circuit, problem, angles, choices_only=True):
    transpiled_circuit = transpile(circuit, backend)
    parameter_dict = to_parameter_dict(angles, circuit)
    statevector = get_statevector(transpiled_circuit, parameter_dict)
    if choices_only:
        probs_dict = statevector.probabilities_dict(range(problem.N))
    else:
        probs_dict = statevector.probabilities_dict()
    return probs_dict

def get_expectation_value(circuit, problem, angles):
    probs_dict = get_probs_dict(circuit, problem, angles)
    obj = partial(objective_function, problem=problem)
    return average_value(probs_dict, obj)

def find_optimal_angles(circuit, problem):
    transpiled_circuit = transpile(circuit, backend)
    obj = partial(objective_function, problem=problem)
    angles_to_parameters = partial(to_parameter_dict, circuit=circuit)
    def angles_to_value(angles):
        parameter_dict = angles_to_parameters(angles)
        statevector = get_statevector(transpiled_circuit, parameter_dict)
        probs_dict = statevector.probabilities_dict()
        value = -average_value(probs_dict, obj)
        return value
    p = circuit.p
    return optimize_angles(p, angles_to_value, circuit.gamma_range(), circuit.beta_range())

def comparable_objective_function(bitstring, problem):
    choice = bitstring_to_choice(bitstring, problem)
    if KnapsackMethod.is_choice_feasible(choice, problem):
        return KnapsackMethod.value(choice, problem)
    return 0

def comparable_expectation_value(problem, probs):
    obj = partial(comparable_objective_function, problem=problem)
    expectation = average_value(probs, obj)
    return expectation

def approximation_ratio(problem, probs):
    expectation = comparable_expectation_value(problem, probs)
    best_known_solutions = KnapsackMethod.classical_solutions(problem)
    choice = best_known_solutions[0]
    best_value = KnapsackMethod.value(choice, problem)
    ratio = expectation / best_value
    return ratio
