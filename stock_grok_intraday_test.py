import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import time

# Fetch hourly ES futures data
stock = yf.download("ES=F", start="2024-01-01",
                    end="2025-02-25", interval="1h")

# Drop any NaN values
stock = stock.dropna()

# Ensure we only use trading hours (6:00 PM–5:00 PM EST, adjust for timezone if needed)
# 6:00 PM–5:00 PM EST (next day)
stock = stock.between_time(time(18, 0), time(16, 59))

# Define ranges for short and long SMAs (tuned for intraday)
short_windows = [1, 2, 3, 4, 5]  # Short SMA: 1–5 hours
long_windows = [5, 10, 15, 20]   # Long SMA: 5–20 hours
results = []

# Function to test SMA strategy and return metrics


def test_sma_strategy(data, short_window, long_window):
    df = data.copy()
    df["Short_SMA"] = df["Close"].rolling(window=short_window).mean()
    df["Long_SMA"] = df["Close"].rolling(window=long_window).mean()

    # Create signals (buy when short SMA > long SMA, sell otherwise)
    df["Signal"] = 0
    df.loc[df["Short_SMA"] > df["Long_SMA"], "Signal"] = 1  # Buy
    df.loc[df["Short_SMA"] < df["Long_SMA"], "Signal"] = -1  # Sell

    # Calculate hourly returns and strategy returns
    df["Returns"] = df["Close"].pct_change()
    df["Strategy_Returns"] = df["Returns"] * df["Signal"].shift(1).fillna(0)

    # Group by trading day to calculate daily returns
    df["Date"] = df.index.date
    daily_returns = df.groupby(
        "Date")["Strategy_Returns"].sum() * 100  # Convert to percentage

    # Calculate cumulative daily returns
    cumulative_daily = (1 + daily_returns / 100).cumprod() - 1
    cumulative_daily_pct = cumulative_daily * 100

    # Risk management: 0.5% stop-loss and 1% take-profit per trade
    df["Position"] = df["Signal"].shift(1).fillna(0)
    df["Trade_Return"] = df["Returns"] * df["Position"]
    df["Cumulative_Trade_Return"] = (1 + df["Trade_Return"]).cumprod() - 1
    df["Daily_Cumulative"] = df.groupby(
        "Date")["Cumulative_Trade_Return"].last() * 100

    # Metrics
    total_days = len(daily_returns)
    success_days = (daily_returns >= 1.0).sum()  # Days hitting 1% or more
    success_rate = (success_days / total_days) * 100 if total_days > 0 else 0
    avg_daily_return = daily_returns.mean()
    max_daily_return = daily_returns.max()
    min_daily_return = daily_returns.min()
    # Annualized Sharpe (24 hours/day)
    sharpe_ratio = avg_daily_return / \
        df["Strategy_Returns"].std() * np.sqrt(24)
    # Max drawdown in %
    max_drawdown = (
        (cumulative_daily_pct / cumulative_daily_pct.cummax() - 1).min())

    return {
        "Short_SMA": short_window,
        "Long_SMA": long_window,
        "Total_Cumulative_Return (%)": cumulative_daily_pct.iloc[-1] if not cumulative_daily_pct.empty else 0,
        "Average_Daily_Return (%)": avg_daily_return,
        "Success_Rate (%)": success_rate,
        "Sharpe_Ratio": sharpe_ratio,
        "Max_Drawdown (%)": max_drawdown,
        "Max_Daily_Return (%)": max_daily_return,
        "Min_Daily_Return (%)": min_daily_return
    }


# Test all SMA combinations
for short in short_windows:
    for long in long_windows:
        if short < long:  # Ensure short SMA is shorter than long SMA
            result = test_sma_strategy(stock, short, long)
            results.append(result)

# Convert results to DataFrame and sort by Total_Cumulative_Return
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(
    by="Total_Cumulative_Return (%)", ascending=False)

# Print top 5 SMA pairs
print("Top 5 SMA Pairs by Total Cumulative Return:")
print(results_df.head())

# Plot the best-performing pair
best_pair = results_df.iloc[0]
best_short = int(best_pair["Short_SMA"])
best_long = int(best_pair["Long_SMA"])

stock["Short_SMA"] = stock["Close"].rolling(window=best_short).mean()
stock["Long_SMA"] = stock["Close"].rolling(window=best_long).mean()
stock["Signal"] = 0
stock.loc[stock["Short_SMA"] > stock["Long_SMA"], "Signal"] = 1
stock["Returns"] = stock["Close"].pct_change()
stock["Strategy_Returns"] = stock["Returns"] * \
    stock["Signal"].shift(1).fillna(0)

stock["Date"] = stock.index.date
daily_returns = stock.groupby("Date")["Strategy_Returns"].sum() * 100
cumulative_daily = (1 + daily_returns / 100).cumprod() - 1
cumulative_daily_pct = cumulative_daily * 100

plt.figure(figsize=(12, 6))
plt.plot(cumulative_daily_pct.index, cumulative_daily_pct,
         label=f"SMA {best_short}/{best_long} Returns")
plt.title(
    f"Best Intraday SMA Strategy: {best_short}-hour vs {best_long}-hour for ES=F")
plt.xlabel("Date")
plt.ylabel("Cumulative Return (%)")
plt.axhline(y=1.0, color='r', linestyle='--', label="1% Daily Target")
plt.legend()
plt.show()

# Plot hourly signals and returns for a sample day (e.g., first trading day in 2024)
sample_day = stock[stock.index.date == pd.Timestamp("2024-01-02").date()]
plt.figure(figsize=(12, 6))
plt.plot(sample_day.index, sample_day["Close"],
         label="Close Price", color="black")
plt.plot(sample_day.index, sample_day["Short_SMA"],
         label=f"{best_short}-hour SMA", color="blue")
plt.plot(sample_day.index, sample_day["Long_SMA"],
         label=f"{best_long}-hour SMA", color="red")
plt.scatter(sample_day.index[sample_day["Signal"] == 1], sample_day["Close"][sample_day["Signal"] == 1],
            color="green", label="Buy Signal", marker="^")
plt.scatter(sample_day.index[sample_day["Signal"] == -1], sample_day["Close"][sample_day["Signal"] == -1],
            color="red", label="Sell Signal", marker="v")
plt.title(
    f"Sample Day (2024-01-02): Price, SMAs, and Signals for SMA {best_short}/{best_long}")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.show()
