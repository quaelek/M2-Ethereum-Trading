import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('Merged_ETH_and_M2_Data.csv')

# Convert the date column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Calculate the percentage change in M2 supply and ETH close price
data['M2_Change'] = data['M2_Supply'].pct_change() * 100
data['ETH_Change'] = data['ETH_Close'].pct_change() * 100

data = data.dropna()

# Calculate moving averages for M2 and ETH percentage changes
data['M2_Change_MA'] = data['M2_Change'].rolling(window=4).mean()
data['ETH_Change_MA'] = data['ETH_Change'].rolling(window=4).mean()

initial_balance = 10000  # USD

# Line A: Final portfolio balance if ETH had been bought on that date and held until the end
portfolio_line_A = []

for i in range(len(data)):
    buy_date = data.iloc[i]['Date']
    buy_price = data.iloc[i]['ETH_Close']
    final_price = data.iloc[-1]['ETH_Close']
    
    eth_balance = initial_balance / buy_price
    final_balance = eth_balance * final_price
    
    portfolio_line_A.append(final_balance)

# Line B: Final portfolio balance using the simple trading strategy starting from each date
portfolio_line_B = []

for i in range(len(data)):
    usd_balance = initial_balance
    eth_balance = 0
    
    for j in range(i, len(data)):
        row = data.iloc[j]
        if row['M2_Change'] > 0:
            # Buy ETH
            if usd_balance > 0:
                eth_balance = usd_balance / row['ETH_Close']
                usd_balance = 0
        elif row['M2_Change'] < 0:
            # Sell ETH
            if eth_balance > 0:
                usd_balance = eth_balance * row['ETH_Close']
                eth_balance = 0
    
    final_balance = usd_balance + (eth_balance * data.iloc[-1]['ETH_Close'])
    portfolio_line_B.append(final_balance)

# Quantify the performance
better_strategy_count = sum(np.array(portfolio_line_B) > np.array(portfolio_line_A))
total_dates = len(portfolio_line_A)
percentage_better = (better_strategy_count / total_dates) * 100

# Stats
mean_line_A = np.mean(portfolio_line_A)
std_line_A = np.std(portfolio_line_A)
mean_line_B = np.mean(portfolio_line_B)
std_line_B = np.std(portfolio_line_B)

# Print and Plot
print(f"Percentage of dates where the simple trading strategy is better: {percentage_better:.2f}%")
print(f"Mean final portfolio value for Buy & Hold: ${mean_line_A:.2f} (±${std_line_A:.2f})")
print(f"Mean final portfolio value for Linear Pro: ${mean_line_B:.2f} (±${std_line_B:.2f})")

plt.figure(figsize=(12, 8))
plt.plot(data['Date'], portfolio_line_A, label='Line A: Buy and Hold')
plt.plot(data['Date'], portfolio_line_B, label='Line B: Linear Proportional')
plt.title('Final Portfolio Balance Over Time')
plt.xlabel('Date')
plt.ylabel('Final Portfolio Balance (USD)')
plt.legend()
plt.grid(True)
plt.show()
