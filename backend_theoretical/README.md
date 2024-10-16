## Quantum Approximate Optimization Algorithm (QAOA)

In combinatorial optimization, QAOA excels as a hybrid quantum-classical algorithm tailored for quantum computing while leveraging classical computing strengths. It effectively addresses NP-hard problems, including Max-Cut, the traveling salesman problem, and quadratic unconstrained binary optimization (QUBO).

### Problem Definition

Given a combinatorial optimization problem involving an N-bit binary string represented as $z = z_1 \ldots z_N$ with a classical objective function $f(z): \{0,1\}^N \rightarrow \mathbb{R}$ to be maximized, the goal is to find a solution $z$ that satisfies the approximation condition: 

$$\frac{f(z)}{f_{\text{max}}} \geq r^*$$

where $f_{\text{max}} = \max_z f(z)$, and $r^*$ is the desired approximation ratio.

### QAOA Algorithm

The QAOA algorithm tackles this problem by encoding the classical objective function $f(z)$ into the phase Hamiltonian $H_c$ to find the optimal eigenvalues:

$$H_c |z\rangle = f(z) |z\rangle$$

Here, $H_c$ operates diagonally on the computational basis states of the $2^N$ dimensional Hilbert space (n-qubit space). The performance of the $p$-level QAOA improves with increasing $p$.

For the $p$-level QAOA, the state $|+\rangle^{\otimes N}$ is initialized, and the Hamiltonians $H_c$ and a mixing Hamiltonian:

$$B = \sum_{j=1}^{N} \sigma_x^j$$

are applied alternately with controlled durations, generating a wave function:

$$|\psi_p(\vec{\gamma}, \vec{\beta})\rangle = e^{-i\beta_p B} e^{-i\gamma_p H_c} \cdots e^{-i\beta_1 B} e^{-i\gamma_1 H_c} |+\rangle^{\otimes N}$$

This variational wave function is parameterized by $2p$ variational parameters, $\gamma$ and $\beta$. The expected value of $H_c$ in this variational state is determined through repeated measurements on a computational basis:

$$f_p(\vec{\gamma}, \vec{\beta}) = \langle \psi_p(\vec{\gamma}, \vec{\beta}) | H_c | \psi_p(\vec{\gamma}, \vec{\beta}) \rangle$$

A classical computer searches for the optimal parameters $(\gamma^*, \beta^*)$ to maximize the averaged output $f(\gamma^*, \beta^*)$:

$$(\gamma^*, \beta^*) = \arg\max_{\vec{\gamma}, \vec{\beta}} f_p(\vec{\gamma}, \vec{\beta})$$

The approximate ratio showing the QAOA performance is given by:

$$r = \frac{f_p(\vec{\gamma}^*, \vec{\beta}^*)}{f_{\text{max}}}$$

Searching for the approximate ratio typically starts with a random initial estimate of the parameters and employs gradient-based optimization.
