Portfolio Simulator
===================

The project implements a simple portfolio simulator that consumes a stream of market prices chunk by chunk and continuously updates the prices of all the related portfolios in scope. 

- The portfolios.csv file defines the entire universe of portfolios.
- Prices.csv stores the market prices of portfolio constituents.
- The results are stamped into the portfolio_prices.csv file.

To generate a sample market prices file, use the following command:

``main.py --app=m``

The market prices are generated using Geometric Brownian Motion and standard normal distribution with starting constituent prices. 
To run the portfolio calculator that calculates the portfolio prices and updates the output CSV file, please run the following command

``main.py --app=p``
