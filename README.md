This project posited that the relationship between the M2 money supply and the Ethereum token (ETH) could be exploited through a trading bot. The goal was to determine if changes in the M2 money supply can be used to predict ETH price movements and develop a trading bot that can outperform a simple buy-and-hold strategy. The project includes analysis and implementation of multiple simple algorithmic trading strategies.

Files in the Repository

1. M2-ETH.pdf

This file contains a report documenting the project's context, trading strategies, and conclusions. The report provides a explanation of the methodologies and results of the project.

2. backtester.py

This script implements the core trading strategies based on the M2 money supply changes. It includes:

    Data preprocessing the data
    Implementing the the trading strategies
    Plotting the performance of each strategy against a buy-and-hold strategy

3. time-independent.py

This script analyzes the time-independence of the trading strategies by starting the trading from various dates and comparing the final portfolio balances. It calculates the percentage of dates where the simple trading strategy outperforms the buy-and-hold strategy, as well as the mean and standard deviation of the final portfolio values for both strategies. As with the backtester, it also exports a graph to visualize the results.

4. Merged_ETH_and_M2_Data.csv

This CSV file contains the historical data of the M2 money supply and Ethereum close prices, which is used as the input for the trading strategies. The columns include:

    The date of the data point
    The M2 money supply value
    The closing price of Ethereum

Installation and Usage
Prerequisites

    Python 3.x
    Pandas
    NumPy
    Matplotlib

Running the Backtester

    Clone the repository and navigate to the project directory.
    Place Merged_ETH_and_M2_Data.csv in the same directory as the scripts.
    Run the backtester.py script to execute the trading strategies and visualize their performance:

    bash

    python backtester.py

Project Structure

├── M2-ETH.py
├── backtester.py
├── time-independent.py
├── Merged_ETH_and_M2_Data.csv
└── README.md

Results and Conclusion

While various trading strategies based on M2 money supply changes can sometimes outperform a buy-and-hold strategy, none of the strategies consistently provided a significant long-term advantage in a time-independent context. The hypothesis that changes in M2 can serve as acute indicators for shifts in ETH prices was not supported by the data. More advanced techniques and data may develop models are unlikely to consistently perform better than the buy-and-hold approach due to changes in asset prices fundamentally being multivariable; while some indicators do perform as signals to asset prices, M2 may not be a strong enough indicator for the value of the ETH token, and to the extent it may have been, it is possible that expectations of M2's growth are usually priced in prior to the M2 figures being posted.
