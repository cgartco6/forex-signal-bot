import yfinance as yf
import pandas as pd
import logging

def fetch_latest_data(symbol: str, period: str = "5m", interval: str = "1m") -> pd.DataFrame:
    """
    Fetch forex data from Yahoo Finance.
    - period: how far back (e.g., "5m", "1h", "1d")
    - interval: candle size (e.g., "1m", "5m")
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        if df.empty:
            logging.warning(f"No data returned for {symbol}")
            return None
        return df
    except Exception as e:
        logging.error(f"Error fetching {symbol}: {e}")
        return None
