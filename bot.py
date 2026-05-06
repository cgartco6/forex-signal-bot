import time
import logging
from config import ACTIVE_PAIRS, SCAN_INTERVAL_SECONDS
from src.data_fetcher import fetch_latest_data
from src.signal_generator import generate_signal
from src.telegram_bot import send_signal_message
from src.risk_manager import no_risk_check   # placeholder, always returns True

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/signals.log"), logging.StreamHandler()]
)

def main():
    logging.info("Starting Forex Signal Bot (1‑minute scalping mode)")
    logging.info(f"Monitoring pairs: {', '.join(ACTIVE_PAIRS)}")

    while True:
        for symbol in ACTIVE_PAIRS:
            # 1. Fetch latest 1m data
            df = fetch_latest_data(symbol, period="5m", interval="1m")
            if df is None or df.empty:
                logging.warning(f"No data for {symbol}")
                continue

            # 2. Generate signal
            signal = generate_signal(df)
            if signal == "WAIT":
                continue

            # 3. Optional risk check (disabled by default)
            if not no_risk_check(symbol, signal):
                logging.info(f"Risk check blocked {signal} on {symbol}")
                continue

            # 4. Send to Telegram immediately
            current_price = df["Close"].iloc[-1]
            send_signal_message(symbol, signal, current_price)

        time.sleep(SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
