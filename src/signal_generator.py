import pandas as pd
from .indicators import add_ema, add_rsi

def generate_signal(df: pd.DataFrame) -> str:
    """
    Generate BUY/SELL/WAIT based on the user's strategy.
    Default: EMA(21) + RSI(14) cross.
    """
    if len(df) < 30:
        return "WAIT"

    # Ensure indicators exist
    df = add_ema(df, 21)
    df = add_rsi(df, 14)

    last = df.iloc[-1]
    price = last["Close"]
    ema21 = last["EMA_21"]
    rsi = last["RSI_14"]

    # === CUSTOMISE THIS SECTION ===
    if price > ema21 and rsi > 50:
        return "BUY"
    elif price < ema21 and rsi < 50:
        return "SELL"
    else:
        return "WAIT"
