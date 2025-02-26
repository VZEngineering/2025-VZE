import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fetch ES futures data
stock = yf.download("ES=F", start="2020-01-01", end="2025-02-25")
stock = stock.dropna()

# Define SMA windows (40 and 150, as per your graph)
stock["SMA40"] = stock["Close"].rolling(window=40).mean()
stock["SMA150"] = stock["Close"].rolling(window=150).mean()

# Create signals (buy when 40-day SMA > 150-day SMA, sell otherwise)
stock["Signal"] = 0
stock.loc[stock["SMA40"] > stock["SMA150"], "Signal"] = 1  # Buy
stock.loc[stock["SMA40"] < stock["SMA150"], "Signal"] = -1  # Sell

# Calculate daily returns
stock["Returns"] = stock["Close"].pct_change()

# Identify buy signals and calculate holding periods in days
buy_signals = stock[stock["Signal"] == 1]
holding_periods_days = []

# Iterate through buy signals to find duration until next sell (or end of data)
for i in range(len(buy_signals)):
    current_date = buy_signals.index[i]

    # Find the next non-buy signal (-1 or 0) after this buy
    mask = stock.index >= current_date
    after_buy = stock.loc[mask]["Signal"]
    sell_date = after_buy[after_buy.ne(1)].index.min(
    ) if not after_buy[after_buy.ne(1)].empty else stock.index[-1]

    if pd.notna(sell_date):
        # Calculate days held
        holding_days = (sell_date - current_date).days
        if holding_days < 0:
            holding_days = 0  # Ensure no negative periods
        holding_periods_days.append(holding_days)
    else:
        # If no sell signal, hold until end of data
        holding_days = (stock.index[-1] - current_date).days
        holding_periods_days.append(holding_days)

# Print results
if holding_periods_days:
    print("Holding Periods (in days) for Each Buy Signal:")
    for i, days in enumerate(holding_periods_days, 1):
        print(f"Purchase {i}: {days} days")

    print(
        f"\nAverage Holding Period: {np.mean(holding_periods_days):.2f} days")
    print(f"Median Holding Period: {np.median(holding_periods_days):.2f} days")
    print(f"Minimum Holding Period: {min(holding_periods_days)} days")
    print(f"Maximum Holding Period: {max(holding_periods_days)} days")
else:
    print("No valid buy signals found.")

# Calculate and plot cumulative returns
cumulative_pct = (
    (1 + stock["Returns"] * stock["Signal"].shift(1).fillna(0)).cumprod() - 1) * 100

plt.figure(figsize=(12, 6))
plt.plot(cumulative_pct.index, cumulative_pct, label="SMA 40/150 Returns")
plt.title("Cumulative Returns for SMA 40/150 Strategy")
plt.xlabel("Date")
plt.ylabel("Cumulative Return (%)")
plt.legend()
plt.show()
