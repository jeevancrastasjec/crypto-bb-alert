import requests
import os
from datetime import datetime

# Binance public endpoint (NO KYC)
BINANCE_URL = "https://data-api.binance.vision/api/v3/klines"

# Telegram secrets
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    r = requests.post(url, json=payload, timeout=10)
    if r.status_code == 200:
        print("📨 Telegram sent")
    else:
        print("❌ Telegram error:", r.text)


def fetch_price(symbol, interval):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 1
    }
    r = requests.get(BINANCE_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return float(data[-1][4])


def main():
    now = datetime.utcnow()
    minute = now.minute

    # BTC → every 15 minutes
    btc_price = fetch_price("BTCUSDT", "15m")
    send_telegram(
        f"📊 BTC Update (15m)\n"
        f"Price: {btc_price}\n"
        f"Time (UTC): {now.strftime('%H:%M')}"
    )

    # SOL → every 30 minutes (only on even 30 mins)
    if minute % 30 == 0:
        sol_price = fetch_price("SOLUSDT", "30m")
        send_telegram(
            f"📊 SOL Update (30m)\n"
            f"Price: {sol_price}\n"
            f"Time (UTC): {now.strftime('%H:%M')}"
        )

    print("✅ Run completed successfully")


if __name__ == "__main__":
    main()
