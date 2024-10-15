import streamlit as st
from datetime import datetime
import pandas as pd
import sys
import os
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import time

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

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .quantum-particle {
        width: 10px;
        height: 10px;
        background-color: #00ff00;
        border-radius: 50%;
        position: absolute;
        animation: quantum-animation 2s infinite ease-in-out;
    }
    @keyframes quantum-animation {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(2); opacity: 0.5; }
        100% { transform: scale(1); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("Quantum Stock Optimization")
st.markdown("Combining **Quantum Computing** with **Mean-Variance Optimization** for stock portfolios.")
# User inputs
st.sidebar.header("Portfolio Selection")
stocks = st.sidebar.text_input("Enter stock tickers (comma-separated)", "AAPL, GOOGL, MSFT, AMZN")
start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime(2023, 1, 1))
budget = st.sidebar.slider("Budget (number of stocks to include)", min_value=1, max_value=len(stocks.split(','))-1, value=1)

# Function to create 3D scatter plot
def create_3d_scatter(stock_list, weights):
    fig = go.Figure(data=[go.Scatter3d(
        x=np.random.rand(len(stock_list)),
        y=np.random.rand(len(stock_list)),
        z=weights,
        mode='markers',
        marker=dict(
            size=weights*50,
            color=weights,
            colorscale='Viridis',
            opacity=0.8
        ),
        text=stock_list,
        hoverinfo='text'
    )])
    fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Weight'),
                      margin=dict(l=0, r=0, b=0, t=0))
    return fig

# Function to create donut chart
def create_donut_chart(stock_list, selected_stocks):
    selected = [1 if stock in selected_stocks else 0 for stock in stock_list]
    fig = go.Figure(data=[go.Pie(labels=stock_list, values=selected, hole=.3)])
    fig.update_traces(textposition='inside', textinfo='label+percent')
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    return fig

if st.sidebar.button("Optimize Portfolio"):
    # Parse stock input
    stock_list = [s.strip().upper() for s in stocks.split(",")]
    
    if len(stock_list) < 2:
        st.error("Please enter at least two stock tickers.")
    elif start_date >= end_date:
        st.error("End date must be after start date.")
    else:
        # Display loading animation
        with st.spinner("Quantum particles are optimizing your portfolio..."):
            start_time = time.time()
            
            # Perform mean-variance optimization
            mv_method = MeanVarianceMethod(stock_list, start_date, end_date)
            optimized_weights = mv_method.weights()
            
            # Call the main quantum function
            higher_prob_key_reversed, higher_prob_key, best_known_solution, approximation_ratio = quantum_main(optimized_weights, budget)
            
            end_time = time.time()
            time_taken = end_time - start_time
            
            # Display results
            st.write("### Quantum Optimization Results")
            st.markdown(f"<span style='color: #00FF00;'>Time taken for optimization: {time_taken:.2f} seconds</span>", unsafe_allow_html=True)
            st.write("#### Optimized Weights")
            optimized_weights_dict = {stock: weight for stock, weight in zip(stock_list, optimized_weights)}
            st.write(optimized_weights_dict)
            
            selected_stocks = [stock for i, stock in enumerate(stock_list) if higher_prob_key_reversed[i] == '1']
            st.write(f"Best known solution: {best_known_solution}")
            st.write(f"Approximation ratio: {approximation_ratio}")

            # Show selected stocks based on higher_prob_key_reversed
            st.write(f"### Suggested Stocks for Portfolio:")
            for stock in selected_stocks:
                st.markdown(f"<span style='background-color: #4CAF50; padding: 5px 10px; border-radius: 20px; margin: 5px;'>{stock}</span>", unsafe_allow_html=True)
            
            st.write("#### Selected Stocks")
            fig_donut = create_donut_chart(stock_list, selected_stocks)
            st.plotly_chart(fig_donut, use_container_width=True)

# Add some final touches
st.sidebar.markdown("---")
st.sidebar.write("Developed with ❤️ using Quantum Computing")