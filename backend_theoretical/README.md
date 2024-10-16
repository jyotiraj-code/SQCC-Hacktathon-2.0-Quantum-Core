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
$$
\sigma^2_i = \frac{1}{N} \sum_{j=1}^{N} \left[R_j - E(R_j)\right]^2
$$
