import streamlit as st
from datetime import datetime, timedelta, date
import sys
import os
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import time
import yfinance as yf

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
st.title("Quantum Portfolio Optimization")
st.markdown("**Quantum Walk Mixer** Based **QAOA** method for Portfolio Optimization")

# User inputs
st.sidebar.header("Portfolio Selection")
stocks = st.sidebar.text_input("Enter stock tickers (comma-separated)", "AAPL, GOOGL, MSFT, AMZN")
# Set min_value to a date earlier than 2010
start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1), min_value=datetime(1900, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime(2023, 1, 1), min_value=datetime(1900, 1, 1))
budget = st.sidebar.slider("Budget (number of stocks to include)", min_value=1, max_value=len(stocks.split(','))-1, value=1)

# Prevent users from entering data beyond today's date
if end_date > date.today():
    st.sidebar.error("End date cannot be beyond today's date.")
    st.stop()

# Color scheme for charts
color_map = px.colors.qualitative.Plotly

def plot_stock_trends(tickers, start_date, end_date):
    for i, ticker in enumerate(tickers):
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            if data.empty:
                st.error(f"No data found for {ticker}. It might be an invalid ticker.")
                continue
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name=ticker, line=dict(color=color_map[i % len(color_map)])))
            fig.update_layout(
                title=f"Historical Stock Prices for {ticker}",
                xaxis_title="Date",
                yaxis_title="Close Price",
                height=400,
                width=800,
                xaxis_rangeslider_visible=True
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")

# Parse stock input and plot trends
stock_list = [s.strip().upper() for s in stocks.split(",")]

# Use an expander to show/hide historical stock trends
with st.expander("Show/Hide Historical Stock Trends", expanded=True):
    plot_stock_trends(stock_list, start_date, end_date)

# Function to create donut chart with unified color and legend order
def create_donut_chart(stock_list, selected_stocks, color_map):
    # Sort stock_list to ensure consistent legend order
    stock_list_sorted = sorted(stock_list)
    
    # Create a selection mask where selected stocks are 1, others 0
    selected = [1 if stock in selected_stocks else 0 for stock in stock_list_sorted]
    
    # Create the donut chart with unified color scheme
    fig = go.Figure(data=[go.Pie(labels=stock_list_sorted, 
                                 values=selected, 
                                 hole=.3, 
                                 marker=dict(colors=[color_map[stock_list.index(stock) % len(color_map)] for stock in stock_list_sorted]))])
    fig.update_traces(textposition='inside', textinfo='label+percent')
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), showlegend=True)
    
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
            try:
                start_time = time.time()
                
                # Perform mean-variance optimization
                mv_method = MeanVarianceMethod(stock_list, start_date, end_date)
                optimized_weights = mv_method.weights()
                
                # Call the main quantum function
                higher_prob_key_reversed, higher_prob_key, best_known_solution, approximation_ratio = quantum_main(optimized_weights, budget)
                
                end_time = time.time()
                time_taken = end_time - start_time
                
                # Hide historical trends
                show_trends = False
                
                # Display results
                st.write("### Quantum Optimization Results")
                st.markdown(f"<span style='color: #00FF00;'>Time taken for optimization: {time_taken:.2f} seconds</span>", unsafe_allow_html=True)
                st.write("#### Optimized Weights")
                optimized_weights_dict = {stock: weight for stock, weight in zip(stock_list, optimized_weights)}
                st.write(optimized_weights_dict)
                
                # Convert best_known_solution to a list, handling the n-d array case
                if isinstance(best_known_solution, np.ndarray):
                    best_known_solution_list = best_known_solution.flatten().tolist()
                else:
                    st.error(f"Unexpected type for best_known_solution: {type(best_known_solution)}")
                    st.write("Best known solution:", best_known_solution)
                    st.stop()
                
                quantum_selected_stocks = [stock for i, stock in enumerate(stock_list) if higher_prob_key_reversed[i] == '1']
                classical_selected_stocks = [stock for i, stock in enumerate(stock_list) if best_known_solution_list[i] == 1]
                
                st.write("### Quantum Method Results and Visualization")
                st.write("#### Quantum Method Selected Stocks:")
                for stock in quantum_selected_stocks:
                    color = color_map[stock_list.index(stock) % len(color_map)]
                    st.markdown(f"<span style='background-color: {color}; padding: 5px 10px; border-radius: 20px; margin: 5px;'>{stock}</span>", unsafe_allow_html=True)
                
                st.write("#### Quantum Method Visualization")
                fig_donut_quantum = create_donut_chart(stock_list, quantum_selected_stocks, color_map)
                st.plotly_chart(fig_donut_quantum, use_container_width=True, key="quantum_donut_1")

                st.write("### Comparison: Quantum vs Classical Method")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("#### Quantum Method Selected Stocks:")
                    for stock in quantum_selected_stocks:
                        color = color_map[stock_list.index(stock) % len(color_map)]
                        st.markdown(f"<span style='background-color: {color}; padding: 5px 10px; border-radius: 20px; margin: 5px;'>{stock}</span>", unsafe_allow_html=True)
                    st.write("#### Quantum Method Visualization")
                    fig_donut_quantum = create_donut_chart(stock_list, quantum_selected_stocks, color_map)
                    st.plotly_chart(fig_donut_quantum, use_container_width=True, key="quantum_donut")
                
                with col2:
                    st.write("#### Classical Method Selected Stocks:")
                    for stock in classical_selected_stocks:
                        color = color_map[stock_list.index(stock) % len(color_map)]
                        st.markdown(f"<span style='background-color: {color}; padding: 5px 10px; border-radius: 20px; margin: 5px;'>{stock}</span>", unsafe_allow_html=True)
                    st.write("#### Classical Method Visualization")
                    fig_donut_classical = create_donut_chart(stock_list, classical_selected_stocks, color_map)
                    st.plotly_chart(fig_donut_classical, use_container_width=True, key="classical_donut")

                st.write("### Performance Comparison")
                st.write(f"Approximation ratio: {approximation_ratio}")
                st.write("The approximation ratio compares the performance of the quantum method to the classical method.")
                st.write("A ratio closer to 1 indicates that the quantum method's performance is closer to the classical method's performance.")
                
                # Calculate the difference in selected stocks
                different_stocks = set(quantum_selected_stocks).symmetric_difference(set(classical_selected_stocks))
                if different_stocks:
                    st.write("### Differences in Stock Selection")
                    st.write("The following stocks were selected differently by the two methods:")
                    
                    for stock in different_stocks:
                        method = "Quantum" if stock in quantum_selected_stocks else "Classical"
                        color = color_map[stock_list.index(stock) % len(color_map)]  # Unified color scheme for the stocks
                        st.markdown(f"<span style='background-color: {color}; padding: 5px 10px; border-radius: 20px; margin: 5px;'>{stock} ({method})</span>", unsafe_allow_html=True)
                else:
                    st.write("### Stock Selection Comparison")
                    st.write("Both methods selected the same stocks for the portfolio.")

            except ValueError as e:
                st.error(f"Error: {str(e)}")
                st.stop()

# Add some final touches
st.sidebar.markdown("---")
st.sidebar.write("Developed with ❤️ using Quantum Computing")
