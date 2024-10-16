from .QAOA import QuantumWalkQAOA
import matplotlib.pyplot as plt

import os
from . import KnapsackMethod
from . import MeanVariance
from . import Utilities
import datetime


def main(er, budget=None):
    p = 1
    m = 5

    if budget is None:
        budget = len(er) // 2

    prices = [1] * len(er)
    problem = KnapsackMethod.KnapsackProblem(er, prices, budget)

    bks = KnapsackMethod.classical_solutions(problem)

    for p in range(1, 6):
        Utilities.is_apply_noise = False

        print(f"Problem: {problem}")
        print("Building Circuit...")
        circuit = QuantumWalkQAOA(problem, p=p, m=m)
        print("Done!")
        print("Optimizing Angles...")
        angles = Utilities.find_optimal_angles(circuit, problem)
        print("Done!")
        print(f"Optimized Angles: {angles}")
        probs = Utilities.get_probs_dict(circuit, problem, angles)
        print(f"Probabilities of Bitstrings: {probs}")
        ratio = Utilities.approximation_ratio(problem, probs)
        print(f"Approximation Ratio: {ratio}")

        os.makedirs("plots", exist_ok=True)
        folder = os.path.join(
            "plots",
            f"{p}_{m}_{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}_NOISELESS",
        )
        os.makedirs(folder, exist_ok=True)
        fig, ax = plt.subplots()
        fig.set_size_inches(18, 10)

        comments = [
            f"Considered {problem}",
            f"QAOA circuit with {p = } and {m = }",
            f"Optimized angles: {angles}",
            f"Resulting Probabilities: {probs}",
            f"Best known solutions: {bks}",
            f"Approximation Ratio: {ratio}",
            f"Higher the probability: {max(probs.values())} at reversed key: {max(probs, key=probs.get)[::-1]}",
            f"Higher the probability: {max(probs.values())} at key: {max(probs, key=probs.get)}",
        ]

        file_name = f"result.txt"
        with open(os.path.join(f"{folder}", file_name), "w") as f:
            f.write("\n".join(comments))
        
        higher_prob_key_reversed = max(probs, key=probs.get)[::-1]
        higher_prob_key = max(probs, key=probs.get)
        best_known_solution = bks
        approximation_ratio = ratio

        return higher_prob_key_reversed, higher_prob_key, best_known_solution, approximation_ratio



if __name__ == "__main__":
    main()
