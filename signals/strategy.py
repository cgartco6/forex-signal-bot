import pandas as pd
import numpy as np

def heikin_ashi(df):
    ha = pd.DataFrame(index=df.index)
    ha['close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    ha['open'] = (df['Open'].shift(1) + df['Close'].shift(1)) / 2
    ha['open'].iloc[0] = df['Open'].iloc[0]
    ha['high'] = df[['High', 'Open', 'Close']].max(axis=1)
    ha['low'] = df[['Low', 'Open', 'Close']].min(axis=1)
    return ha

def detect_signals(df, ma_period=20, stoch_k=14, stoch_d=3):
    """
    Returns (pre_signal, main_signal)
    pre_signal: 'BUY_SETUP', 'SELL_SETUP', or None
    main_signal: 'BUY', 'SELL', or None
    """
    # 1. MA(20)
    df['MA20'] = df['Close'].rolling(window=ma_period).mean()
    
    # 2. Stochastic
    low_min = df['Low'].rolling(window=stoch_k).min()
    high_max = df['High'].rolling(window=stoch_k).max()
    df['%K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
    df['%D'] = df['%K'].rolling(window=stoch_d).mean()
    
    # 3. Heikin Ashi
    ha = heikin_ashi(df)
    
    last = df.iloc[-1]
    prev = df.iloc[-2]
    ha_last = ha.iloc[-1]
    
    # ---------- MAIN SIGNAL (Katie's original) ----------
    main_buy = (
        last['Close'] > last['MA20'] and
        last['%K'] < 20 and
        last['%K'] > prev['%K'] and
        last['%K'] > last['%D'] and
        ha_last['close'] > ha_last['open']
    )
    main_sell = (
        last['Close'] < last['MA20'] and
        last['%K'] > 80 and
        last['%K'] < prev['%K'] and
        last['%K'] < last['%D'] and
        ha_last['close'] < ha_last['open']
    )
    
    # ---------- PRE‑SIGNAL (early warning, 1-3 candles earlier) ----------
    # Buy Setup: price > MA20, %K < 20 (oversold), but %K still below %D (not yet crossing)
    pre_buy = (
        last['Close'] > last['MA20'] and
        last['%K'] < 20 and
        last['%K'] < last['%D']    # not crossed yet
    )
    # Sell Setup: price < MA20, %K > 80 (overbought), but %K still above %D
    pre_sell = (
        last['Close'] < last['MA20'] and
        last['%K'] > 80 and
        last['%K'] > last['%D']
    )
    
    pre_signal = None
    if pre_buy:
        pre_signal = 'BUY_SETUP'
    elif pre_sell:
        pre_signal = 'SELL_SETUP'
    
    main_signal = None
    if main_buy:
        main_signal = 'BUY'
    elif main_sell:
        main_signal = 'SELL'
    
    return pre_signal, main_signal
