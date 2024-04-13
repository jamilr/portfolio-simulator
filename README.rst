Portfolio Calculator
=============================
To generate the market prices file, please use the following command:

main.py --app=m

To run the portfolio calculator that calculates the portfolio prices
and updates the output csv file, portfolio_prices.csv, please run teh following command

main.pu --app=p

Market Data Generation

The market prices generator uses Geometric Brownian Motion to simulate the asset prices path.
The starting market prices are dated as of Friday, April 5th; end of the day close prices.