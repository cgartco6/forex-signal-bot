# Forex Signal Bot – 1‑Minute Scalping Signals to Telegram

This bot generates **continuous trading signals** for major forex pairs (EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD, USD/CHF) based on a simple EMA + RSI strategy. It sends **BUY** or **SELL** alerts to a Telegram chat **before** the trade would be executed, allowing you to manually trade on a demo account.

> ⚠️ **No risk management is implemented** – the bot only produces signals. Use it for learning and testing on a demo account only.

## Strategy (placeholder – modify freely)
- Timeframe: 1‑minute candles  
- Enter BUY when price > EMA(21) and RSI(14) > 50  
- Enter SELL when price < EMA(21) and RSI(14) < 50  
- Signals are sent instantly when conditions are met (every minute).

## Setup

1. Clone the repo  
2. Create a virtual environment and install dependencies:  
   ```bash
   pip install -r requirements.txt
