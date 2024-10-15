from functools import partial
from itertools import product
from fractions import Fraction
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import Aer, transpile, execute
from qiskit.circuit import Parameter
import numpy as np
import math
from KnapsackMethod import KnapsackProblem

class QFT(QuantumCircuit):
    def __init__(self, register):
        super().__init__(register, name="QFT")
        for idx, qubit in reversed(list(enumerate(register))):
            super().h(qubit)
            for c_idx, control_qubit in reversed(list(enumerate(register[:idx]))):
                k = idx - c_idx + 1
                super().cp(2 * np.pi / 2**k, qubit, control_qubit)

class Add(QuantumCircuit):
    def __init__(self, register, n, control=None):
        self.register = register
        self.control = control
        qubits = [*register, *control] if control is not None else register
        super().__init__(qubits, name=f"Add {n}")
        binary = list(map(int, reversed(bin(n)[2:])))
        for idx, value in enumerate(binary):
            if value:
                self._add_power_of_two(idx)

    def _add_power_of_two(self, k):
        phase_gate = super().p
        if self.control is not None:
            phase_gate = partial(super().cp, target_qubit=self.control)
        for idx, qubit in enumerate(self.register):
            l = idx + 1
            if l > k:
                m = l - k
                phase_gate(2 * np.pi / 2**m, qubit)

class FeasibilityOracle(QuantumCircuit):
    def __init__(self, choice_reg, weight_reg, flag_qubit, problem, clean_up=True):
        c = math.floor(math.log2(problem.max_weight)) + 1
        w0 = 2**c - problem.max_weight - 1
        subcirc = QuantumCircuit(choice_reg, weight_reg, name="")
        qft = QFT(weight_reg)
        subcirc.append(qft.to_instruction(), weight_reg)
        for qubit, weight in zip(choice_reg, problem.weights):
            adder = Add(weight_reg, weight, control=[qubit]).to_instruction()
            subcirc.append(adder, [*weight_reg, qubit])
        adder = Add(weight_reg, w0)
        subcirc.append(adder.to_instruction(), weight_reg)
        subcirc.append(qft.inverse().to_instruction(), weight_reg)
        super().__init__(choice_reg, weight_reg, flag_qubit, name="U_v")
        super().append(subcirc.to_instruction(), [*choice_reg, *weight_reg])
        super().x(weight_reg[c:])
        super().mcx(weight_reg[c:], flag_qubit)
        super().x(weight_reg[c:])
        if clean_up:
            super().append(subcirc.inverse().to_instruction(), [*choice_reg, *weight_reg])

class SingleQubitQuantumWalk(QuantumCircuit):
    def __init__(self, choice_reg, weight_reg, flag_regs, problem: KnapsackProblem, j: int):
        flag_x, flag_neighbor, flag_both = flag_regs
        self.beta = Parameter("beta")
        super().__init__(choice_reg, weight_reg, *flag_regs, name=f"SingleQubitQuantumWalk_{j=}")
        feasibility_oracle = FeasibilityOracle(choice_reg, weight_reg, flag_x, problem)
        super().append(feasibility_oracle.to_instruction(), [*choice_reg, *weight_reg, flag_x])
        super().x(choice_reg[j])
        super().append(feasibility_oracle.to_instruction(), [*choice_reg, *weight_reg, flag_neighbor])
        super().x(choice_reg[j])
        super().ccx(flag_x, flag_neighbor, flag_both)
        super().crx(2 * self.beta, flag_both, choice_reg[j])
        super().ccx(flag_x, flag_neighbor, flag_both)
        super().x(choice_reg[j])
        super().append(feasibility_oracle.to_instruction(), [*choice_reg, *weight_reg, flag_neighbor])
        super().x(choice_reg[j])
        super().append(feasibility_oracle.to_instruction(), [*choice_reg, *weight_reg, flag_x])

class QuantumWalkMixer(QuantumCircuit):
    def __init__(self, choice_reg, weight_reg, flag_regs, problem: KnapsackProblem, m: int):
        flag_x, flag_neighbor, flag_both = flag_regs
        self.beta = Parameter("beta")
        super().__init__(choice_reg, weight_reg, *flag_regs, name=f"QuantumWalkMixer_{m=}")
        for __ in range(m):
            for j in range(problem.N):
                jwalk = SingleQubitQuantumWalk(choice_reg, weight_reg, flag_regs, problem, j)
                super().append(jwalk.to_instruction({jwalk.beta: self.beta / m}), [*choice_reg, *weight_reg, *flag_regs])

class DephaseValue(QuantumCircuit):
    def __init__(self, choice_reg, problem):
        self.gamma = Parameter("gamma")
        super().__init__(choice_reg, name="Dephase Value")
        for qubit, value in zip(choice_reg, problem.values):
            super().p(- self.gamma * value, qubit)
