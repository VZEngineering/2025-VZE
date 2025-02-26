import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Fetch data
stock = yf.download("SPY", start="2023-01-01", end="2025-02-25")

# Handle missing values
stock.dropna(inplace=True)

# SMAs and strategy
stock["SMA50"] = stock["Close"].rolling(window=50).mean()
stock["SMA200"] = stock["Close"].rolling(window=200).mean()
stock["Signal"] = 0
stock.loc[stock["SMA50"] > stock["SMA200"], "Signal"] = 1
stock["Returns"] = stock["Close"].pct_change()
stock["Strategy_Returns"] = stock["Returns"] * stock["Signal"].shift(1)
cumulative = (1 + stock["Strategy_Returns"]).cumprod()

# Handle missing values after adding new columns
stock.dropna(inplace=True)

# AI prediction
stock["SMA_Diff"] = stock["SMA50"] - stock["SMA200"]
stock["Target"] = (stock["Returns"] > 0).astype(int)
features = stock[["SMA_Diff", "Returns"]].dropna()
target = stock["Target"].loc[features.index]
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.3, random_state=42)
model = RandomForestClassifier().fit(X_train, y_train)
predictions = model.predict(X_test)

# Plot
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(cumulative, label="Strategy Returns")
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(y_test.index, y_test, label="Actual")
plt.plot(y_test.index, predictions, label="Predicted")
plt.legend()
plt.show()
