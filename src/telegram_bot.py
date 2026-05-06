import logging
from telegram import Bot
from telegram.error import TelegramError
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_signal_message(symbol: str, signal: str, price: float) -> bool:
    """
    Send formatted signal to Telegram.
    """
    symbol_clean = symbol.replace("=X", "")
    emoji = "🚀 BUY" if signal == "BUY" else "📉 SELL"
    message = (
        f"<b>{emoji} SIGNAL</b>\n"
        f"Pair: {symbol_clean}\n"
        f"Price: {price:.5f}\n"
        f"Action: {signal}\n"
        f"Time: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="HTML")
        logging.info(f"Signal sent: {symbol} {signal} @ {price}")
        return True
    except TelegramError as e:
        logging.error(f"Telegram error: {e}")
        return False

# Need pandas for timestamp
import pandas as pd
