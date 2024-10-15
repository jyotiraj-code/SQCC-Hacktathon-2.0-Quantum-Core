import numpy as np

class KnapsackEncoding:
    def __init__(self, values, weights, max_weight):
        self.values = values
        self.weights = weights
        self.max_weight = max_weight
        self.total_weight = sum(self.weights)
        self.N = len(self.weights)

def itemvalue(choice, problem):
    """Return the value of an item choice.
        Assumes choice is a numpy array of length problem.N"""
    return choice.dot(problem.values)

def itemweight(choice, problem):
    """Return the weight of an item choice.
        Assumes choice is a numpy array of length problem.N"""
    return choice.dot(problem.weights)

def feasibility_check(choice, problem):
    return itemweight(choice, problem) <= problem.max_weight

def classical_solutions(problem: KnapsackEncoding):
    def choices_from_number(problem, number):
        return np.array(list(map(int, list(reversed(bin(number)[2:])))) + [0] * (problem.N - len(bin(number)[2:])))
    best = 0
    solutions = []
    for i in range(2**problem.N):
        choice = choices_from_number(problem, i)
        value = choice.dot(problem.values)
        weight = choice.dot(problem.weights)
        is_legal = weight <= problem.max_weight
        if is_legal and value > best:
            best = value
            solutions = [choice]
        elif is_legal and value == best:
            solutions.append(choice)
    return np.array(solutions)
