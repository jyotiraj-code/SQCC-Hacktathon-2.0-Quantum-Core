import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pypfopt import risk_models
from pypfopt import expected_returns
from scipy.optimize import minimize


class CVaROptimization:
    def __init__(self, stocks, start_date, end_date, confidence_level=0.95):
        ohlc = yf.download(stocks, start=start_date, end=end_date)
        self.stocks = stocks
        self.prices = ohlc["Adj Close"].dropna(how="all")
        self.confidence_level = confidence_level

    def calculate_portfolio_return(self, weights):
        """Calculate the expected portfolio return based on weights."""
        returns = self.prices.pct_change().dropna()
        portfolio_return = np.dot(returns.mean(), weights)
        return portfolio_return

    def calculate_cvar(self, weights):
        """Calculate Conditional Value at Risk (CVaR)."""
        returns = self.prices.pct_change().dropna()
        portfolio_returns = returns.dot(weights)

        # Calculate the VaR at the specified confidence level
        var = np.percentile(portfolio_returns, (1 - self.confidence_level) * 100)

        # Calculate the CVaR
        cvar = portfolio_returns[portfolio_returns <= var].mean()
        return -cvar  # We return negative CVaR for minimization

    def optimize_weights(self):
        """Optimize the portfolio weights to minimize CVaR."""
        num_assets = len(self.stocks)
        initial_weights = np.ones(num_assets) / num_assets  # Equal initial weights

        # Constraints: weights sum to 1
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for asset in range(num_assets))  # No short-selling

        # Optimize
        result = minimize(self.calculate_cvar, initial_weights, 
                          method='SLSQP', bounds=bounds, constraints=constraints)

        return result.x  # Return optimized weights


# Example usage
if __name__ == "__main__":
    stocks = ["AAPL", "GOOGL", "MSFT", "AMZN"]
    start_date = "2020-01-01"
    end_date = "2023-01-01"
    
    cvar_optimizer = CVaROptimization(stocks, start_date, end_date)
    optimized_weights = cvar_optimizer.optimize_weights()
    
    print("Optimized Weights:", optimized_weights)

