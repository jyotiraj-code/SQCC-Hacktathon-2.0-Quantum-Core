import streamlit as st
from datetime import datetime
import pandas as pd

import sys
import os
from pathlib import Path

# Get the absolute path of the current file (app.py)
current_file = Path(__file__).resolve()

# Get the parent directory of the current file (App directory)
parent_directory = current_file.parent

# Get the parent directory of the App directory (project root)
project_root = parent_directory.parent

# Add the project root to sys.path
sys.path.append(str(project_root))

from backend_theoretical.MeanVariance import MeanVarianceMethod
from backend_theoretical.main import main as quantum_main

# Streamlit app configuration
st.set_page_config(page_title="Quantum Stock Optimization", layout="wide")

# Title and description
st.title("Quantum Stock Optimization")
st.markdown("Combining **Quantum Computing** with **Mean-Variance Optimization** for stock portfolios.")

# User inputs
st.sidebar.header("Portfolio Selection")
stocks = st.sidebar.text_input("Enter stock tickers (comma-separated)", "AAPL, GOOGL, MSFT, AMZN")
start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime(2023, 1, 1))
budget = st.sidebar.slider("Budget (number of stocks to include)", min_value=1, max_value=len(stocks.split(','))-1, value=1)

if st.sidebar.button("Optimize Portfolio"):
    # Parse stock input
    stock_list = [s.strip().upper() for s in stocks.split(",")]

    if len(stock_list) < 2:
        st.error("Please enter at least two stock tickers.")
    elif start_date >= end_date:
        st.error("End date must be after start date.")
    else:
        st.write("### Optimizing Portfolio")
        # Perform mean-variance optimization
        mv_method = MeanVarianceMethod(stock_list, start_date, end_date)
        optimized_weights = mv_method.weights()
        st.write("Optimized Weights for Mean-Variance Portfolio:")
        st.write(dict(zip(stock_list, optimized_weights)))

        # Call the main quantum function
        higher_prob_key_reversed, higher_prob_key, best_known_solution, approximation_ratio = quantum_main(optimized_weights, budget)

        # Display results
        st.write("### Quantum Optimization Results")
        st.write(f"Higher probability key (reversed): {higher_prob_key_reversed}")
        st.write(f"Higher probability key: {higher_prob_key}")
        st.write(f"Best known solution: {best_known_solution}")
        st.write(f"Approximation ratio: {approximation_ratio}")

        # Show selected stocks based on higher_prob_key_reversed
        selected_stocks = [stock for i, stock in enumerate(stock_list) if higher_prob_key_reversed[i] == '1']
        st.write(f"### Suggested Stocks for Portfolio: {', '.join(selected_stocks)}")
