import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fetch ES futures data
stock = yf.download("ES=F", start="2020-01-01", end="2025-02-25")
stock = stock.dropna()

# Define ranges for short and long SMAs
short_windows = [5, 10, 20, 30, 40, 50]
long_windows = [50, 100, 150, 200]
results = []

# Function to calculate strategy returns


def test_sma_strategy(data, short_window, long_window):
    df = data.copy()
    df["Short_SMA"] = df["Close"].rolling(window=short_window).mean()
    df["Long_SMA"] = df["Close"].rolling(window=long_window).mean()
    df["Signal"] = 0
    df.loc[df["Short_SMA"] > df["Long_SMA"], "Signal"] = 1  # Buy
    df.loc[df["Short_SMA"] < df["Long_SMA"], "Signal"] = -1  # Sell
    df["Returns"] = df["Close"].pct_change()
    df["Strategy_Returns"] = df["Returns"] * df["Signal"].shift(1)
    cumulative = (1 + df["Strategy_Returns"].fillna(0)
                  ).cumprod().iloc[-1] - 1  # Total return
    sharpe = df["Strategy_Returns"].mean() / df["Strategy_Returns"].std() * \
        np.sqrt(252)  # Annualized Sharpe
    return cumulative * 100, sharpe  # Return as percentage


# Test all combinations
for short in short_windows:
    for long in long_windows:
        if short < long:  # Ensure short SMA is shorter than long SMA
            total_return, sharpe = test_sma_strategy(stock, short, long)
            results.append({
                "Short_SMA": short,
                "Long_SMA": long,
                "Total_Return (%)": total_return,
                "Sharpe_Ratio": sharpe
            })

# Convert results to DataFrame
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by="Total_Return (%)", ascending=False)

# Display top 5 results
print("Top 5 SMA Pairs by Total Return:")
print(results_df.head())

# Plot the best pair
best_pair = results_df.iloc[0]
best_short = int(best_pair["Short_SMA"])
best_long = int(best_pair["Long_SMA"])
stock["Short_SMA"] = stock["Close"].rolling(window=best_short).mean()
stock["Long_SMA"] = stock["Close"].rolling(window=best_long).mean()
stock["Signal"] = 0
stock.loc[stock["Short_SMA"] > stock["Long_SMA"], "Signal"] = 1
stock["Returns"] = stock["Close"].pct_change()
stock["Strategy_Returns"] = stock["Returns"] * stock["Signal"].shift(1)
cumulative_pct = (
    (1 + stock["Strategy_Returns"].fillna(0)).cumprod() - 1) * 100

plt.figure(figsize=(12, 6))
plt.plot(cumulative_pct.index, cumulative_pct,
         label=f"SMA {best_short}/{best_long} Returns")
plt.title(f"Best SMA Strategy: {best_short}-day vs {best_long}-day")
plt.xlabel("Date")
plt.ylabel("Cumulative Return (%)")
plt.legend()
plt.show()
