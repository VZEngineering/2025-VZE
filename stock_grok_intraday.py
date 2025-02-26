import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import time

# Fetch hourly ES futures data (yfinance may have limitations, so this is a starting point)
stock = yf.download("ES=F", start="2024-01-01",
                    end="2025-02-25", interval="1h")

# Drop any NaN values
stock = stock.dropna()

# Ensure we only use trading hours (6:00 PM–5:00 PM EST, adjust for timezone if needed)
# Note: yfinance hourly data might not perfectly align with ES trading hours; we'll filter later if needed
# 6:00 PM–5:00 PM EST (next day)
stock = stock.between_time(time(18, 0), time(16, 59))

# Define SMA windows (short: 1 hour, long: 15 hours, tuned for intraday)
stock["SMA1"] = stock["Close"].rolling(window=1).mean()
stock["SMA15"] = stock["Close"].rolling(window=15).mean()

# Create signals (buy when 1-hour SMA > 15-hour SMA, sell otherwise)
stock["Signal"] = 0
stock.loc[stock["SMA1"] > stock["SMA15"], "Signal"] = 1  # Buy
stock.loc[stock["SMA1"] < stock["SMA15"], "Signal"] = -1  # Sell

# Calculate hourly returns
stock["Returns"] = stock["Close"].pct_change()

# Strategy returns (shift Signal by 1 to avoid look-ahead bias)
stock["Strategy_Returns"] = stock["Returns"] * \
    stock["Signal"].shift(1).fillna(0)

# Group by trading day to calculate daily cumulative returns
stock["Date"] = stock.index.date
daily_returns = stock.groupby(
    "Date")["Strategy_Returns"].sum() * 100  # Convert to percentage

# Calculate cumulative daily returns
cumulative_daily = (1 + daily_returns / 100).cumprod() - 1
cumulative_daily_pct = cumulative_daily * 100  # Convert to percentage

# Add risk management: 0.5% stop-loss and 1% take-profit per trade
stock["Position"] = stock["Signal"].shift(1).fillna(0)
stock["Trade_Return"] = stock["Returns"] * stock["Position"]
stock["Cumulative_Trade_Return"] = (1 + stock["Trade_Return"]).cumprod() - 1
stock["Daily_Cumulative"] = stock.groupby(
    "Date")["Cumulative_Trade_Return"].last() * 100

# Check if we hit 1% daily (or adjust for partial days)
target_return = 1.0  # 1% target per day
success_days = (daily_returns >= target_return).sum()
total_days = len(daily_returns)
success_rate = (success_days / total_days) * 100 if total_days > 0 else 0

# Print results
print(f"Number of Trading Days: {total_days}")
print(f"Days Achieving 1% or More: {success_days}")
print(f"Success Rate: {success_rate:.2f}%")
print(f"Average Daily Return: {daily_returns.mean():.2f}%")
print(f"Maximum Daily Return: {daily_returns.max():.2f}%")
print(f"Minimum Daily Return: {daily_returns.min():.2f}%")

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(cumulative_daily_pct.index, cumulative_daily_pct,
         label="Cumulative Daily Returns (%)")
plt.title("Intraday SMA 1/15 Strategy for ES=F (Hourly Data)")
plt.xlabel("Date")
plt.ylabel("Cumulative Return (%)")
plt.axhline(y=target_return, color='r', linestyle='--', label="1% Target")
plt.legend()
plt.show()

# Plot hourly signals and returns for a sample day (e.g., first trading day in 2024)
sample_day = stock[stock.index.date == pd.Timestamp("2024-01-02").date()]
plt.figure(figsize=(12, 6))
plt.plot(sample_day.index, sample_day["Close"],
         label="Close Price", color="black")
plt.plot(sample_day.index, sample_day["SMA1"],
         label="1-hour SMA", color="blue")
plt.plot(sample_day.index, sample_day["SMA15"],
         label="15-hour SMA", color="red")
plt.scatter(sample_day.index[sample_day["Signal"] == 1], sample_day["Close"][sample_day["Signal"] == 1],
            color="green", label="Buy Signal", marker="^")
plt.scatter(sample_day.index[sample_day["Signal"] == -1], sample_day["Close"][sample_day["Signal"] == -1],
            color="red", label="Sell Signal", marker="v")
plt.title("Sample Day (2024-01-02): Price, SMAs, and Signals")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.show()
