# Import required libraries
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from pypfopt import risk_models, expected_returns, EfficientFrontier
from .KnapsackMethod import KnapsackProblem

class MeanVarianceMethod:
    def __init__(self, stocks, start_date, end_date):
        ohlc = yf.download(stocks, start=start_date, end=end_date)
        self.stocks = stocks
        self.prices = ohlc["Adj Close"].dropna(how="all")
        
    def covariance(self):
        cov = risk_models.CovarianceShrinkage(self.prices).ledoit_wolf()
        return cov

    def expected_returns(self):
        mu = expected_returns.capm_return(self.prices)
        return mu

    def weights(self):
        er = self.expected_returns()
        cov = self.covariance()

        ef = EfficientFrontier(er, cov, weight_bounds=(None, None))
        ef.min_volatility()
        weights = ef.clean_weights()
        return list(weights.values())

# # Example usage
# if __name__ == "__main__":
#     stocks = ["AAPL", "GOOGL", "MSFT", "AMZN"]
#     start_date = "2020-01-01"
#     end_date = "2023-01-01"
    
#     mv_method = MeanVarianceMethod(stocks, start_date, end_date)
#     optimized_weights = mv_method.weights()
    
#     print("Optimized Weights for Mean-Variance Portfolio as a list:")
#     print(optimized_weights)
