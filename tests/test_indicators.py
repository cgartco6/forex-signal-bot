import pandas as pd
from src.indicators import add_ema, add_rsi

def test_ema():
    df = pd.DataFrame({"Close": [1.0, 2.0, 3.0, 4.0, 5.0]})
    df = add_ema(df, 3)
    assert "EMA_3" in df.columns
    assert not df["EMA_3"].isna().all()

def test_rsi():
    df = pd.DataFrame({"Close": [10, 11, 12, 11, 10, 9, 8, 9, 10, 11, 12, 13, 14, 15, 16]})
    df = add_rsi(df, 14)
    assert "RSI_14" in df.columns
    assert 0 <= df["RSI_14"].iloc[-1] <= 100
