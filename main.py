import time
import logging
from datetime import datetime
import yfinance as yf
from signals.strategy import detect_signals
from telegram_bot.bot import send_setup, send_main_signal

MAJOR_PAIRS = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X', 'NZDUSD=X', 'USDCHF=X']

# Stores last sent pre-signal to avoid spamming
last_pre_signal = {}

def get_1min_data(pair):
    ticker = yf.Ticker(pair)
    return ticker.history(period='2h', interval='1m')

def run_loop():
    logging.basicConfig(level=logging.INFO)
    
    while True:
        for pair in MAJOR_PAIRS:
            try:
                df = get_1min_data(pair)
                pre_signal, main_signal = detect_signals(df)
                
                price = df['Close'].iloc[-1]
                ma = df['MA20'].iloc[-1]
                k = df['%K'].iloc[-1]
                d = df['%D'].iloc[-1]
                ha_color = 'GREEN 🌿' if pre_signal == 'BUY_SETUP' else 'RED 🔥'
                ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
                
                # Send pre-signal only once per pair (resets when conditions disappear)
                if pre_signal and last_pre_signal.get(pair) != pre_signal:
                    send_setup(pair.replace('=X',''), pre_signal, price, ma, k, d, ts)
                    last_pre_signal[pair] = pre_signal
                elif not pre_signal:
                    last_pre_signal[pair] = None
                
                # Send main signal immediately when conditions are met
                if main_signal:
                    send_main_signal(pair.replace('=X',''), main_signal, price, ma, k, d, ha_color, ts)
                    
            except Exception as e:
                logging.error(f"Error on {pair}: {e}")
        
        time.sleep(60)  # scan every minute

if __name__ == '__main__':
    run_loop()
