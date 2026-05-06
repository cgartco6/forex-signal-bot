import os
import logging
from telegram import Bot, ParseMode
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = Bot(token=BOT_TOKEN)

def send_setup(currency_pair, signal_type, price, ma_value, stoch_k, stoch_d, timestamp):
    """Send early warning setup indicator"""
    direction = "POTENTIAL LONG" if signal_type == "BUY_SETUP" else "POTENTIAL SHORT"
    color = "🟡" if signal_type == "BUY_SETUP" else "🟠"
    
    msg = f"""
{color} *SETUP ALERT* {color}
📌 *{currency_pair}* – {direction}

💵 *Price:* {price:.5f}
📈 *MA(20):* {ma_value:.5f}
⚡ *Stochastic:* %K={stoch_k:.1f} | %D={stoch_d:.1f}
⏰ *Time:* {timestamp}

⚠️ Conditions are aligning. Watch for full entry signal.
    """
    try:
        bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logging.error(f"Setup send failed: {e}")

def send_main_signal(currency_pair, signal_type, price, ma_value, stoch_k, stoch_d, ha_color, timestamp):
    """Send actual entry signal (Katie's original)"""
    emoji = '🟢' if signal_type == 'BUY' else '🔴'
    direction = 'ENTER LONG 🔼' if signal_type == 'BUY' else 'ENTER SHORT 🔽'
    
    msg = f"""
{emoji} *SIGNAL: {signal_type} {currency_pair}* {emoji}

📊 *Direction:* {direction}
💵 *Entry Price:* {price:.5f}
📈 *MA(20):* {ma_value:.5f}
⚡ *Stochastic:* %K={stoch_k:.1f} | %D={stoch_d:.1f}
🕯️ *Heikin Ashi:* {ha_color}
⏰ *Time:* {timestamp}

⚠️ *Risk is high* – no stop loss per Katie's method.
    """
    try:
        bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.MARKDOWN)
        logging.info(f"Main signal sent: {signal_type} {currency_pair}")
    except Exception as e:
        logging.error(f"Main signal send failed: {e}")
