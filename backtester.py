import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read CSV file into DataFrame
data = pd.read_csv('Merged_ETH_and_M2_Data.csv')

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Filter for data from March 2020 onwards
data = data[data['Date'] >= '2020-03-01']

# Rename columns for clarity
data = data.rename(columns={'M2_Supply': 'M2_Supply', 'ETH_Close': 'ETH_Close'})

# Calculate percentage changes for M2 supply and ETH price
data['M2_Change'] = data['M2_Supply'].pct_change() * 100
data['ETH_Change'] = data['ETH_Close'].pct_change() * 100

# Remove rows with NaN values from percentage changes
data = data.dropna()

# Calculate 4-period moving averages for percentage changes
data['M2_Change_MA'] = data['M2_Change'].rolling(window=4).mean()
data['ETH_Change_MA'] = data['ETH_Change'].rolling(window=4).mean()

# Initialize trading variables
initial_balance = 10000  # Starting USD balance
eth_balance = 0          # Starting ETH balance
usd_balance = initial_balance
portfolio_values = []    # Track portfolio value

# Linear proportional trading strategy
for index, row in data.iterrows():
    m2_change = row['M2_Change']
    eth_price = row['ETH_Close']
    
    if m2_change > 0:
        if usd_balance > 0:
            eth_balance = usd_balance / eth_price
            usd_balance = 0
    elif m2_change < 0:
        if eth_balance > 0:
            usd_balance = eth_balance * eth_price
            eth_balance = 0
    
    # Compute and store portfolio value
    portfolio_value = usd_balance + (eth_balance * eth_price)
    portfolio_values.append(portfolio_value)

# Add portfolio values to DataFrame
data['Portfolio_Value'] = portfolio_values

# Reinitialize for tiered thresholds strategy
initial_balance = 10000
eth_balance = 0
usd_balance = initial_balance
portfolio_values_tiered_thresholds = []

# Tiered thresholds trading strategy
for index, row in data.iterrows():
    m2_change_ma = row['M2_Change_MA']
    eth_price = row['ETH_Close']
    
    if pd.notna(m2_change_ma):
        if m2_change_ma > 0:
            if m2_change_ma <= 0.3:
                usd_to_use = usd_balance * 0.10
            elif m2_change_ma <= 0.5:
                usd_to_use = usd_balance * 0.25
            elif m2_change_ma <= 0.7:
                usd_to_use = usd_balance * 0.50
            elif m2_change_ma <= 1.0:
                usd_to_use = usd_balance * 0.75
            else:
                usd_to_use = usd_balance
            
            eth_balance += usd_to_use / eth_price
            usd_balance -= usd_to_use
        
        elif m2_change_ma < 0:
            if m2_change_ma >= -0.3:
                eth_to_sell = eth_balance * 0.10
            elif m2_change_ma >= -0.5:
                eth_to_sell = eth_balance * 0.25
            elif m2_change_ma >= -0.7:
                eth_to_sell = eth_balance * 0.50
            elif m2_change_ma >= -1.0:
                eth_to_sell = eth_balance * 0.75
            else:
                eth_to_sell = eth_balance
            
            usd_balance += eth_to_sell * eth_price
            eth_balance -= eth_to_sell
    
    # Compute and store portfolio value
    portfolio_value = usd_balance + (eth_balance * eth_price)
    portfolio_values_tiered_thresholds.append(portfolio_value)

# Add tiered threshold portfolio values to DataFrame
data['Portfolio_Value_tiered_thresholds'] = portfolio_values_tiered_thresholds


# Define the moving_average_granular trading strategy
initial_balance = 10000  #  USD
eth_balance = 0          # ETH
usd_balance = initial_balance

# List to track portfolio value over time
portfolio_values_moving_average_granular = []

# Define the linear function for trade percentage
def calculate_trade_percentage(m2_change, max_threshold=2.0):
    clamped_change = max(-max_threshold, min(m2_change, max_threshold))
    # Calculate the trade percentage (range 0 to 1)
    trade_percentage = abs(clamped_change) / max_threshold
    return trade_percentage

# moving_average_granular trading strategy
for index, row in data.iterrows():
    m2_change_ma = row['M2_Change_MA']
    eth_price = row['ETH_Close']
    
    if pd.notna(m2_change_ma):
        trade_percentage = calculate_trade_percentage(m2_change_ma)
        
        if m2_change_ma > 0:
            # Buy ETH based on the trade percentage
            usd_to_use = usd_balance * trade_percentage
            eth_balance += usd_to_use / eth_price
            usd_balance -= usd_to_use
        elif m2_change_ma < 0:
            # Sell ETH based on the trade percentage
            eth_to_sell = eth_balance * trade_percentage
            usd_balance += eth_to_sell * eth_price
            eth_balance -= eth_to_sell

    # Calculate portfolio value
    portfolio_value = usd_balance + (eth_balance * eth_price)
    portfolio_values_moving_average_granular.append(portfolio_value)

# Add balance to the dataframe
data['Portfolio_Value_moving_average_granular'] = portfolio_values_moving_average_granular

# Define non-linear functions
def exponential_trade_percentage(m2_change, k=1.0):
    clamped_change = max(-2.0, min(m2_change, 2.0))  # Clamp to a reasonable range
    trade_percentage = np.exp(abs(clamped_change) / k) - 1
    return min(trade_percentage, 1)  # Ensure trade percentage does not exceed 1

def logarithmic_trade_percentage(m2_change, k=10.0):
    clamped_change = max(-2.0, min(m2_change, 2.0))  
    trade_percentage = np.log(1 + abs(clamped_change) * k)
    return min(trade_percentage, 1)

def polynomial_trade_percentage(m2_change, k=1.0, n=2):
    clamped_change = max(-2.0, min(m2_change, 2.0))
    trade_percentage = (abs(clamped_change) / k)**n
    return min(trade_percentage, 1)

# non-linear trading strategy for exponential function
initial_balance = 10000 
eth_balance = 0          
usd_balance = initial_balance
portfolio_values_exponential = []

for index, row in data.iterrows():
    m2_change_ma = row['M2_Change_MA']
    eth_price = row['ETH_Close']
    
    if pd.notna(m2_change_ma):
        trade_percentage = exponential_trade_percentage(m2_change_ma, k=0.5)
        
        if m2_change_ma > 0:
            usd_to_use = usd_balance * trade_percentage
            eth_balance += usd_to_use / eth_price
            usd_balance -= usd_to_use
        elif m2_change_ma < 0:
            eth_to_sell = eth_balance * trade_percentage
            usd_balance += eth_to_sell * eth_price
            eth_balance -= eth_to_sell

    portfolio_value = usd_balance + (eth_balance * eth_price)
    portfolio_values_exponential.append(portfolio_value)

# logarithmic function
initial_balance = 10000  
eth_balance = 0          
usd_balance = initial_balance
portfolio_values_logarithmic = []

for index, row in data.iterrows():
    m2_change_ma = row['M2_Change_MA']
    eth_price = row['ETH_Close']
    
    if pd.notna(m2_change_ma): 
        trade_percentage = logarithmic_trade_percentage(m2_change_ma, k=5.0)
        
        if m2_change_ma > 0:
            usd_to_use = usd_balance * trade_percentage
            eth_balance += usd_to_use / eth_price
            usd_balance -= usd_to_use
        elif m2_change_ma < 0:
            eth_to_sell = eth_balance * trade_percentage
            usd_balance += eth_to_sell * eth_price
            eth_balance -= eth_to_sell

    portfolio_value = usd_balance + (eth_balance * eth_price)
    portfolio_values_logarithmic.append(portfolio_value)

#  polynomial function
initial_balance = 10000  
eth_balance = 0         
usd_balance = initial_balance
portfolio_values_polynomial = []

for index, row in data.iterrows():
    m2_change_ma = row['M2_Change_MA']
    eth_price = row['ETH_Close']
    
    if pd.notna(m2_change_ma): 
        trade_percentage = polynomial_trade_percentage(m2_change_ma, k=1.0, n=2)
        
        if m2_change_ma > 0:
            usd_to_use = usd_balance * trade_percentage
            eth_balance += usd_to_use / eth_price
            usd_balance -= usd_to_use
        elif m2_change_ma < 0:
            eth_to_sell = eth_balance * trade_percentage
            usd_balance += eth_to_sell * eth_price
            eth_balance -= eth_to_sell

    portfolio_value = usd_balance + (eth_balance * eth_price)
    portfolio_values_polynomial.append(portfolio_value)

#  ETH balance for buy and hold 
initial_eth_price = data['ETH_Close'].iloc[0]
initial_eth_balance = initial_balance / initial_eth_price

# portfolio value for buy and hold
portfolio_values_buy_hold = data['ETH_Close'] * initial_eth_balance
data['Portfolio_Value_Buy_Hold'] = portfolio_values_buy_hold

# Plot the portfolio values
plt.figure(figsize=(12, 8))

# Plot 'Buy and Hold' line
plt.plot(data['Date'], data['Portfolio_Value_Buy_Hold'], label='Buy and Hold', color='black', linewidth=2)

# Plot each strategye
strategies = {
    'Simple Strategy': data['Portfolio_Value'],
    'tiered_thresholds Strategy': data['Portfolio_Value_tiered_thresholds'],
    'moving_average_granular Strategy': data['Portfolio_Value_moving_average_granular'],
    'Exponential Strategy': portfolio_values_exponential,
    'Logarithmic Strategy': portfolio_values_logarithmic,
    'Polynomial Strategy': portfolio_values_polynomial
}

for label, values in strategies.items():
    plt.plot(data['Date'], values, label=label)
    plt.fill_between(data['Date'], data['Portfolio_Value_Buy_Hold'], values,
                     where=(values >= data['Portfolio_Value_Buy_Hold']), facecolor='blue', alpha=0.3, interpolate=True)
    plt.fill_between(data['Date'], data['Portfolio_Value_Buy_Hold'], values,
                     where=(values < data['Portfolio_Value_Buy_Hold']), facecolor='red', alpha=0.3, interpolate=True)

plt.title('Portfolio Value Over Time (Trading Based on M2 Changes)')
plt.xlabel('Date')
plt.ylabel('Portfolio Value (USD)')
plt.legend()
plt.grid(True)
plt.show()

final_portfolio_value_exponential = portfolio_values_exponential[-1]
final_portfolio_value_logarithmic = portfolio_values_logarithmic[-1]
final_portfolio_value_polynomial = portfolio_values_polynomial[-1]

final_portfolio_value_exponential, final_portfolio_value_logarithmic, final_portfolio_value_polynomial

# Print
final_date = data['Date'].iloc[-1]
print(f"Final portfolio balances as of {final_date}:")
print(f"Buy and Hold: {data['Portfolio_Value_Buy_Hold'].iloc[-1]:.2f} USD")
for label, values in strategies.items():
    if isinstance(values, list):
        final_balance = values[-1]
    else:
        final_balance = values.iloc[-1]
    print(f"{label}: {final_balance:.2f} USD")