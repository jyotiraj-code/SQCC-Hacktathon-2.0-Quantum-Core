from functools import partial
from itertools import product
from fractions import Fraction
from qiskit import QuantumRegister, QuantumCircuit
from qiskit.circuit import Parameter
import numpy as np
import math
from .KnapsackMethod import KnapsackProblem
from .Circuits import Dephase, QWMixer

class QuantumWalkQAOA(QuantumCircuit):
    def __init__(self, problem: KnapsackProblem, p: int, m: int):
        self.p = p
        self.m = m
        self.betas = [Parameter(f"beta{i}") for i in range(p)]
        self.gammas = [Parameter(f"gamma{i}") for i in range(p)]
        n = math.floor(math.log2(problem.total_weight)) + 1
        c = math.floor(math.log2(problem.max_weight)) + 1
        if c == n:
            n += 1
        choice_reg = QuantumRegister(problem.N, name="choice")
        weight_reg = QuantumRegister(n, name="weight")
        flag_x = QuantumRegister(1, name="v(x)")
        flag_neighbor = QuantumRegister(1, name="v(n_j(x))")
        flag_both = QuantumRegister(1, name="v_j(x)")
        flag_regs = [flag_x, flag_neighbor, flag_both]
        print("Number of qubits:", len(choice_reg) + len(weight_reg) + len(flag_regs))
        super().__init__(choice_reg, weight_reg, *flag_regs, name=f"QuantumWalkQAOA {m=},{p=}")
        phase_circ = Dephase(choice_reg, problem)
        mix_circ = QWMixer(choice_reg, weight_reg, flag_regs, problem, m)
        for gamma, beta in zip(self.gammas, self.betas):
            super().append(phase_circ.to_instruction({phase_circ.gamma: gamma}), choice_reg)
            super().append(mix_circ.to_instruction({mix_circ.beta: beta}), [*choice_reg, *weight_reg, *flag_regs])
        super().save_statevector()
        super().measure_all()

    def beta_range(self):
        return 0, self.m * math.pi

    @staticmethod
    def gamma_range():
        return 0, 2 * math.pi
