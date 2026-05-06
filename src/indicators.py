import pandas as pd

def add_ema(df: pd.DataFrame, period: int, column: str = "Close") -> pd.DataFrame:
    """Add Exponential Moving Average to DataFrame."""
    df[f"EMA_{period}"] = df[column].ewm(span=period, adjust=False).mean()
    return df

def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Add Relative Strength Index (RSI)."""
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    df[f"RSI_{period}"] = 100 - (100 / (1 + rs))
    return df

def add_sma(df: pd.DataFrame, period: int) -> pd.DataFrame:
    """Add Simple Moving Average."""
    df[f"SMA_{period}"] = df["Close"].rolling(window=period).mean()
    return df
