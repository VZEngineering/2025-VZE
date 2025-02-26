import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Fetch data
stock = yf.download("ES=F", start="2020-01-01", end="2025-02-25")

# Handle missing values
stock.dropna(inplace=True)

# SMAs and strategy
stock["SMA50"] = stock["Close"].rolling(window=40).mean()
stock["SMA200"] = stock["Close"].rolling(window=150).mean()
stock["Signal"] = 0
stock.loc[stock["SMA50"] > stock["SMA200"], "Signal"] = 1
stock["Returns"] = stock["Close"].pct_change()
stock["Strategy_Returns"] = stock["Returns"] * stock["Signal"].shift(1)
cumulative = (1 + stock["Strategy_Returns"]).cumprod()  # Growth factor
cumulative_pct = (cumulative - 1) * 100  # Convert to percentage

# Handle missing values after adding new columns
stock.dropna(inplace=True)

# AI prediction
stock["SMA_Diff"] = stock["SMA50"] - stock["SMA200"]
stock["Target"] = (stock["Returns"] > 0).astype(int)
features = stock[["SMA_Diff", "Returns"]].dropna()
target = stock["Target"].loc[features.index]
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.3, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Print accuracy
print("Prediction Accuracy:", model.score(X_test, y_test))

# Plot
plt.figure(figsize=(12, 8))

# Top plot: Strategy Returns in Percentage
plt.subplot(2, 1, 1)
plt.plot(cumulative_pct.index, cumulative_pct, label="Strategy Returns")
plt.title("Cumulative Returns from SMA Crossover Strategy")
plt.xlabel("Date")
plt.ylabel("Cumulative Return (%)")
plt.legend()

# Bottom plot: Actual vs Predicted (scatter)
plt.subplot(2, 1, 2)
plt.scatter(y_test.index, y_test, label="Actual Direction",
            color="blue", alpha=0.5, s=10)
plt.scatter(y_test.index, predictions, label="Predicted Direction",
            color="orange", alpha=0.5, s=10)
plt.title("Actual vs Predicted Price Direction (0 = Down, 1 = Up)")
plt.xlabel("Date")
plt.ylabel("Direction")
plt.legend()

plt.tight_layout()
plt.show()
