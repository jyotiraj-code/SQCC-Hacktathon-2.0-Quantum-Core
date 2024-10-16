# Quantum Walk Mixer Based Quantum Apporximate Optimization Algorithm using a Knapsack Encoding Method

The financial backbone of an economy heavily relies on its financial system. In the financial industry, **Portfolio Optimization** is a key process that strategically allocates assets to achieve optimal returns while minimizing risks. It involves diversifying assets to offset individual risk profiles, a crucial element in the investment process [1].

## Key Methods

Our approach introduces the following methods:

- **Knapsack Problem Formulation:** The portfolio selection problem is reformulated as a knapsack problem, incorporating the expected return from the Markowitz model and setting the capacity based on the knapsack framework.
  
- **Quantum Walk Mixer-based QAOA:** We apply a Quantum Walk Mixer-based QAOA for the knapsack problem, utilizing a shallow circuit layer to reduce computational complexity and improve solution quality.

## Knapsack Problem in Portfolio Optimization

In this context, we adapt the knapsack encoding by treating all portfolio assets as items, where:
- **Profit:** The expected return of each asset, estimated using historical data or forecasting techniques.
- **Weights:** The risk associated with each asset, typically measured by the asset's standard deviation or variance-covariance matrix.
- **Knapsack Capacity:** This represents the available capital, budget, or the number of stocks that can be invested in.

The goal of this reformulation is to maximize the total portfolio value (profit) while satisfying the capacity constraint and potentially other constraints, such as a target return or a minimum number of assets.

## Portfolio Optimization Process

The portfolio optimization process includes the following steps:

1. **Asset Selection:** Identifying suitable assets for investment.
2. **Return Projections:** Estimating future returns using historical data.
3. **Risk Quantification:** Assessing the uncertainty associated with each asset.
4. **Optimization:** Selecting the optimal portfolio that maximizes expected returns for a given risk level.

## Markowitz Model

One of the most studied models in portfolio optimization is the Markowitz model, represented as:


$$R_i = \sum_{t=1}^{\infty} d_{it} r_{it}$$

Here, 
- $r_{it}$ indicates anticipated return at time t  per stock invested in
- $d_{it}$ is the rate at which return in the $i_{th}$ security where time t is discounted back to presents.

The Standard Deviation is a statistical measure used as an indicator of the
uncertainty or risk linked to return. It is illustrated as: 
$$\sigma^2_i = \frac{1}{N} \sum_{j=1}^{N}\left[R_j - E(R_j)\right]^2$$

The covariance of returns measures the relative riskiness of a security within a portfolio of
securities, suppose for two securities we will have: $$\sigma_{ij} = E\left[(R_i - E(R_i))(R_j - E(R_j))\right]$$

## Quantum Approximate Optimization Algorithm (QAOA)

In combinatorial optimization, QAOA excels as a hybrid quantum-classical algorithm tailored for quantum computing while leveraging classical computing strengths. It effectively addresses NP-hard problems, including Max-Cut, the traveling salesman problem, and quadratic unconstrained binary optimization (QUBO).

### Problem Definition

Given a combinatorial optimization problem involving an N-bit binary string represented as $ z = z_1 \ldots z_N $ with a classical objective function $ f(z): \{0,1\}^N \rightarrow \mathbb{R} $ to be maximized, the goal is to find a solution $ z $ that satisfies the approximation condition:

$$
\frac{f(z)}{f_{\text{max}}} \geq r^*
$$

where $ f_{\text{max}} = \max_z f(z) $, and $ r^* $ is the desired approximation ratio.

### QAOA Algorithm

The QAOA algorithm tackles this problem by encoding the classical objective function $ f(z) $ into the phase Hamiltonian $ H_c $ to find the optimal eigenvalues:

$$
H_c |z\rangle = f(z) |z\rangle
$$

Here, $ H_c $ operates diagonally on the computational basis states of the $ 2^N $ dimensional Hilbert space (n-qubit space). The performance of the $ p $-level QAOA improves with increasing $ p $.

For the $ p $-level QAOA, the state $ |+\rangle^{\otimes N} $ is initialized, and the Hamiltonians $ H_c $ and a mixing Hamiltonian:

$$
B = \sum_{j=1}^{N} \sigma_x^j
$$

are applied alternately with controlled durations, generating a wave function:

$$
|\psi_p(\vec{\gamma}, \vec{\beta})\rangle = e^{-i\beta_p B} e^{-i\gamma_p H_c} \cdots e^{-i\beta_1 B} e^{-i\gamma_1 H_c} |+\rangle^{\otimes N}
$$

This variational wave function is parameterized by $ 2p $ variational parameters, $ \gamma $ and $ \beta $. The expected value of $ H_c $ in this variational state is determined through repeated measurements on a computational basis:

$$
f_p(\vec{\gamma}, \vec{\beta}) = \langle \psi_p(\vec{\gamma}, \vec{\beta}) | H_c | \psi_p(\vec{\gamma}, \vec{\beta}) \rangle
$$

A classical computer searches for the optimal parameters $ (\gamma^*, \beta^*) $ to maximize the averaged output $ f(\gamma^*, \beta^*) $:

$$
(\gamma^*, \beta^*) = \arg\max_{\vec{\gamma}, \vec{\beta}} f_p(\vec{\gamma}, \vec{\beta})
$$

The approximate ratio showing the QAOA performance is given by:

$$
r = \frac{f_p(\vec{\gamma}^*, \vec{\beta}^*)}{f_{\text{max}}}
$$

Searching for the approximate ratio typically starts with a random initial estimate of the parameters and employs gradient-based optimization.



## THE CODE IMPLEMENTATION:

### `MeanVariance.py` and `KnapsackMethod.py` 

The formulation for changing the problem to a knapsack problem is based on the fundamental principles of Mean-Variance optimization which focuses on the Markowitz Model. This model historically maximizes the anticipated yield of a portfolio while considering a predetermined level of risk, quantified by the variance of
portfolio returns. We denoted the expected return $E(R_{i})$ of stock i by using the mean-variance calculation. Next up, formulating to a Knapsack Problem. We have the following mathematical transformation:

$$
R(x) = \sum_{i=1}^{n} x_i E(R_i)
$$

subject to the constraint:

$$
\sum_{i=1}^{n} x_i w_i \leq C,
$$

where:
- $x_i$ represents the decision variables,
- $E(R_i)$ denotes the expected return of asset $i$,
- $w_i$ represents the weight or risk associated with asset $i$,
- $C$ is the capacity constraint.

Now,
Knapsack module implements the Knapsack problem. The key components of this implementation are:

- **KnapsackProblem**: A data class that encapsulates the values, weights, and maximum weight of the knapsack. The constructor uses the `__post_init__` method to initialize `total_weight` and `N` (the number of items).
  
- **value(choice, problem)**: Computes the total value of a given choice of assets.
  
- **weight(choice, problem)**: Computes the total weight of a given choice of assets.
  
- **is_choice_feasible(choice, problem)**: Checks if a given choice of assets does not exceed the maximum weight constraint.
  
- **classical_solutions(problem: KnapsackProblem)**: Evaluates all possible combinations of asset choices to find the optimal selection that maximizes return without exceeding the weight constraint.

### MeanVariance.py

The `MeanVariance.py` module uses the Mean-Variance optimization method to calculate optimized portfolio weights based on historical stock data. The main components include:

- **MeanVarianceMethod**: A class that encapsulates the Mean-Variance optimization logic. It initializes by downloading stock data for the specified date range using Yahoo Finance.

- **covariance()**: Computes the covariance matrix of the stock returns using a shrinkage method.

- **expected_returns()**: Calculates the expected returns of the assets using the CAPM approach.

- **weights()**: Computes the optimal weights for the assets in the portfolio using the Efficient Frontier method.



### `Circuits.py` and `QAOA.py`

- Feasibility Oracle: It is used as a hypothetical subroutine that instantly determines whether a proposed solution to the knapsack problem violates and constraints.
  We define $K(N) = \{0,1\}^N$ as the set of all possible bitstrings of length $N$ representing potential portfolio choices. Each possible choice of any of the $N$ items is represented by a bitstring $x \in K(N)$.

Consequently, the subset of feasible solutions is denoted as $F$ for the knapsack problem, and the feasibility function is defined as:

$$
f : K(N) \rightarrow \{0,1\}, \quad x \mapsto f(x) =
\begin{cases}
1, & \text{if } x \in F, \\
0, & \text{otherwise.}
\end{cases}
$$

Moreover, the feasibility oracle, which is unitary, $U_f$, can be described as:

$$
U_f |x, y\rangle = |x, y \oplus w(x)\rangle, \quad \forall x \in K(N), \, y \in K(1)
$$

In portfolio optimization, a state $|x\rangle$ represents a specific stock allocation, deemed feasible if $x \in F$ and the total weight $w(x)$ does not exceed the capacity $C$. The feasibility oracle toggles a flag qubit $|y\rangle$ based on the feasibility of the state $|x\rangle$, indicating the portfolio configuration.

We allocate qubits as follows:
- $S$: records the knapsack choices.
- $K_w$: holds the weight of the item choice.
- $K_F$: serves as the flag qubit for the feasibility of state $S$.

The total number of qubits required is $Q_S + Q_w + Q_F$. The total weight $w(x)$ is computed by adding the weights of items controlled by the bits in register $S$, followed by an inequality check using a multiple-controlled NOT gate:

$$
w(x) \leq C \iff w(x) + C_0 < C + C_0 + 1
$$

This condition ensures that the binary representation of $w(x) + C_0$ has zeros in all positions beyond $k$.

The feasibility oracle $U_f$ utilizes two primary unitary operations:
- $U_1$: augments $K_w$ with a predetermined offset $C_0$, utilizing Quantum Fourier Transform (QFT) for weight addition.
- $U_2$: applied conditionally based on the outcome of $U_1$.

The process begins by initializing the ancillary weight register $K_w$ to $|0\rangle$. Quantum Fourier Transform (QFT) is then applied to $K_w$ to prepare it for quantum addition, although QFT does not alter the state of $|0\rangle$. This step is crucial for preparing nonzero initial states of $K_w$. 

After transforming $K_w$ from the computational basis to the Fourier basis, the weight representation distributes across the amplitude of the quantum state:

$$
\text{QFT} |K_w\rangle = \frac{1}{\sqrt{2^n}} \sum_{k=0}^{2^n-1} e^{2\pi i \cdot 0 \cdot k / 2^n} |k\rangle
$$

Weights are then added to $\text{QFT} |K_w\rangle$ through controlled operations involving phase rotations, conditioned on the bits of the bitstring $x$ that indicate item selections. Each bit in $x$ determines whether the corresponding weight $w_i$ should be added to $K_w$. This addition in the Fourier space involves phase rotations executed by a sequence of controlled phase gates, where the magnitude of the rotation depends on $w_i$ and the position of the controlling bit. A controlled phase rotation is applied to $K_w$ for each selected item (where the corresponding bit in $x$ is $|1\rangle$).


The phase added to each computational basis state $|k\rangle$ within $K_w$ is proportional to $w_i$:

$$
|K_w\rangle =
\begin{cases}
|K_w + w_i\rangle, & \text{if } x_i = 1, \\
|K_w\rangle, & \text{otherwise.}
\end{cases}
$$

This phase rotation encodes the addition of $w_i$ into the quantum state. After this process, the register is transformed back to the computational basis using the inverse QFT:

$$
\text{QFT}^{-1} |K_w\rangle
$$

The inverse QFT decodes the phase information back into a computational state representing the total weight of the selected items. While QFT encodes the weight as a superposition of phases, the inverse QFT converts these phases back into a binary number representing the sum of the weights. The final state of the register $K_w$ after applying $U_1$ is:

$$
U_1 |x, 0, y\rangle = |x, w(x) + C_0, y\rangle
$$

- The Quantum Walk Mixers:
The mixing operator $U_B(\beta) = e^{-i\beta B}$ is generated by the mixing Hamiltonian $B$, which is defined as:

$$
B |x\rangle = \sum_{i=0}^{N-1} f_i(x) |n_i(x)\rangle, \quad \forall x \in K(N)
$$

Here, $n_i(x)$ is the $i^{th}$ neighbor of $x$. The inner product for neighboring states is given by:

$$
\langle x | B | x' \rangle =
\begin{cases}
1, & \text{if } \text{Ham}(x, x') = 1, \\
0, & \text{otherwise}
\end{cases}
$$

To implement the mixing operator $U_B(\beta)$ effectively, we use an alternative operator $\tilde{B}$, constructed from $V_i$ and its inverse $V_i^\dagger$, to encode feasibility information of neighboring states into auxiliary qubits for controlled state manipulation. The operator also includes single-qubit $X_i$ gates for exploring neighboring states. The feasible oracle $U_f$ ensures only valid states are mixed, and $R_{X_i}(2\beta)$ adjusts the amplitudes of states based on feasibility, refining the mixing process. Auxiliary qubits store feasibility information.

The `Circuits.py` module implements a quantum algorithm for solving the knapsack problem using various quantum components. The main components include:

- **QFT Class**: Implements the Quantum Fourier Transform used in the feasibility oracle and quantum walk mixers, facilitating efficient quantum state processing.

- **Addition Class**: Represents the quantum addition operation used to compute the total weight of the selected items, maintaining the quantum properties during the addition of states.

- **FbsOracle Class**: Implements the feasibility oracle functionality that determines whether the selected items meet the knapsack constraints, guiding the quantum search process.

- **SQQW Class**: Represents a single-qubit quantum walk that adjusts the amplitude based on the feasibility of neighboring states, enabling effective exploration of the state space.

- **QWMixer Class**: Implements the quantum walk mixer that refines the amplitudes of states based on feasibility conditions, enhancing the convergence towards optimal solutions in the quantum algorithm.
