import json
import requests
import math
from datetime import datetime

BINANCE_API = "https://api.binance.com/api/v3/klines"
TELEGRAM_API = "https://api.telegram.org"

# Loaded from GitHub Secrets
BOT_TOKEN = "${{ secrets.TELEGRAM_BOT_TOKEN }}"
CHAT_ID = "${{ secrets.TELEGRAM_CHAT_ID }}"

def send_telegram(message):
    url = f"{TELEGRAM_API}/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def get_klines(symbol, interval="4h", limit=50):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(BINANCE_API, params=params)
    return response.json()

def bollinger_bands(closes, period=20, multiplier=2):
    sma = sum(closes[-period:]) / period
    variance = sum((x - sma) ** 2 for x in closes[-period:]) / period
    std_dev = math.sqrt(variance)
    upper = sma + multiplier * std_dev
    lower = sma - multiplier * std_dev
    return sma, upper, lower

def main():
    with open("coins.json") as f:
        config = json.load(f)

    send_telegram("✅ TEST ALERT: Bot is running correctly")

    threshold = config["alertThreshold"]

    for coin in config["coins"]:
        if not coin["enabled"]:
            continue

        symbol = coin["symbol"]
        klines = get_klines(symbol)

        # Ignore current forming candle
        closed_candles = klines[:-1]
        closes = [float(c[4]) for c in closed_candles]

        last_close = closes[-1]
        sma, upper, lower = bollinger_bands(closes)

        if last_close >= upper * threshold:
            time = datetime.utcfromtimestamp(closed_candles[-1][6] / 1000)
            message = (
                f"🚨 BB ALERT (4H)\n\n"
                f"Coin: {symbol}\n"
                f"Close: {last_close:.2f}\n"
                f"Upper BB: {upper:.2f}\n"
                f"Time: {time} UTC"
            )
           

if __name__ == "__main__":
    main()
