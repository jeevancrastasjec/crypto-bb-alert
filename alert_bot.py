import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    r = requests.post(url, json=payload)
    if not r.ok:
        print("❌ Telegram error:", r.text)
    else:
        print("✅ Telegram message sent")

def get_price(coin_id: str):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()[coin_id]["usd"]

def main():
    now = datetime.utcnow()
    minute = now.minute

    messages = []

    # BTC every 15 minutes
    if minute % 15 == 0:
        btc_price = get_price("bitcoin")
        messages.append(f"🟠 <b>BTC</b> price (15m)\n💲 {btc_price:,} USD")

    # SOL every 30 minutes
    if minute % 30 == 0:
        sol_price = get_price("solana")
        messages.append(f"🟣 <b>SOL</b> price (30m)\n💲 {sol_price:,} USD")

    if messages:
        final_message = "⏰ <b>Crypto Price Update</b>\n\n" + "\n\n".join(messages)
        send_telegram(final_message)
    else:
        print("ℹ️ No alerts this run")

if __name__ == "__main__":
    main()
