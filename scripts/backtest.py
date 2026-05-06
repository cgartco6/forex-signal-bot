"""
Simple backtesting script to evaluate signal performance on historical data.
Run: python scripts/backtest.py --pair EURUSD=X --period 7d
"""
import argparse
import pandas as pd
from src.data_fetcher import fetch_latest_data
from src.signal_generator import generate_signal

def backtest(symbol: str, days: int = 7):
    df = fetch_latest_data(symbol, period=f"{days}d", interval="1m")
    if df is None:
        print("No data")
        return

    signals = []
    for i in range(30, len(df)):
        window = df.iloc[:i+1]
        sig = generate_signal(window)
        signals.append(sig)

    df = df.iloc[30:].copy()
    df["signal"] = signals

    # Count signals
    buy_signals = (df["signal"] == "BUY").sum()
    sell_signals = (df["signal"] == "SELL").sum()
    print(f"Backtest for {symbol} over {days} days:")
    print(f"  BUY signals: {buy_signals}")
    print(f"  SELL signals: {sell_signals}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", default="EURUSD=X")
    parser.add_argument("--period", default="7d")
    args = parser.parse_args()
    backtest(args.pair, int(args.period.replace("d", "")))
