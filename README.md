# Quantum Stock Optimization

Quantum Stock Optimization is a Streamlit-based web application that combines Quantum Computing with Mean-Variance Optimization for stock portfolios. This innovative tool allows users to optimize their stock portfolios using advanced quantum algorithms.

# Deployed link - https://qwm-qaoa-based-portfolio-optimization.onrender.com/

> **Note on Performance:**
> 
> The project is deployed on a free service with limited computing resources, which may result in extended processing times. For example:
> 
> - On the deployed version: The default placeholder data may take over 1 minute to process.
> - On a local system: Performance can be significantly better. For instance, on an M1 MacBook Air, the same operation takes approximately 5 seconds.
> 
> For optimal performance and faster results, we recommend running the application locally on a system with adequate computational power.

This project was built for [Quantathon 2.0](https://quantathon-o.devfolio.co/) under the Quantum-core track. The problem statement addressed is "Portfolio Optimization based on Quantum Walks".

## Features

- Input multiple stock tickers
- Select date range for historical data
- Adjust budget (number of stocks to include)
- Quantum-enhanced portfolio optimization
- Interactive visualizations of results

## Theoretical Background

For more detailed information about the theoretical aspects of this project, including the quantum algorithms and optimization techniques used, please refer to the [Backend Theory README](./backend_theoretical/README.md).

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- pip (Python package manager)

## Installation

To install Quantum Stock Optimization, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/quantum-stock-optimization.git
   cd quantum-stock-optimization
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the Quantum Stock Optimization app:

1. From the root folder:
   ```
   streamlit run App/app.py
   ```

2. From inside the App folder:
   ```
   cd App
   streamlit run app.py
   ```

The application will open in your default web browser. Enter stock tickers, adjust the date range and budget, then click "Optimize Portfolio" to see the results.

## Contributing

Contributions to Quantum Stock Optimization are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [NumPy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Quantathon 2.0](https://quantathon-o.devfolio.co/)
