import json
import requests
import math
import os
from datetime import datetime

# APIs
BINANCE_API = "https://api.binance.com/api/v3/klines"
TELEGRAM_API = "https://api.telegram.org"

# Secrets (from GitHub Actions)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_telegram(message):
    url = f"{TELEGRAM_API}/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)


def get_klines(symbol, interval="4h", limit=50):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(BINANCE_API, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def bollinger_bands(closes, period=20, multiplier=2):
    sma = sum(closes[-period:]) / period
    variance = sum((x - sma) ** 2 for x in closes[-period:]) / period
    std_dev = math.sqrt(variance)
    upper = sma + multiplier * std_dev
    lower = sma - multiplier * std_dev
    return sma, upper, lower


def main():
    # Load config
    with open("coins.json", "r") as f:
        config = json.load(f)

    # 🔎 TEST MESSAGE (REMOVE AFTER CONFIRMATION)
    send_telegram("✅ TEST ALERT: Bot is running correctly")
    return

    threshold = config["alertThreshold"]

    for coin in config["coins"]:
        if not coin.get("enabled", False):
            continue

        symbol = coin["symbol"]

        klines = get_klines(symbol)
        closed_candles = klines[:-1]  # ignore forming candle
        closes = [float(candle[4]) for candle in closed_candles]

        last_close = closes[-1]
        _, upper, _ = bollinger_bands(closes)

        if last_close >= upper * threshold:
            close_time = datetime.utcfromtimestamp(
                closed_candles[-1][6] / 1000
            )

            message = (
                f"🚨 BB ALERT (4H)\n\n"
                f"Coin: {symbol}\n"
                f"Close: {last_close:.2f}\n"
                f"Upper BB: {upper:.2f}\n"
                f"Time: {close_time} UTC"
            )

            send_telegram(message)


if __name__ == "__main__":
    main()
