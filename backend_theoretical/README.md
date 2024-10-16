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
