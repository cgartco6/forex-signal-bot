import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Major forex pairs (Yahoo Finance symbols)
ALL_PAIRS = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X",
    "AUDUSD=X",
    "USDCAD=X",
    "USDCHF=X"
]

# Choose which pairs to monitor
ACTIVE_PAIRS = ALL_PAIRS   # or a subset like ["EURUSD=X", "GBPUSD=X"]

# How often to check for new signals (seconds)
SCAN_INTERVAL_SECONDS = 60   # every minute
