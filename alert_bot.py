import requests
import statistics
import os

# Binance public endpoint (NO KYC, works on GitHub Actions)
BINANCE_URL = "https://data-api.binance.vision/api/v3/klines"

# Telegram secrets (from GitHub Secrets)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

PAIRS = [
    {"symbol": "BTCUSDT", "interval": "15m"},
    {"symbol": "SOLUSDT", "interval": "30m"}
]

BB_PERIOD = 20
BB_STD_DEV = 2


def send_telegram(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram credentials missing")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    r = requests.post(url, json=payload, timeout=10)
    if r.status_code != 200:
        print("❌ Telegram error:", r.text)
    else:
        print("📨 Telegram alert sent")


def fetch_closes(symbol, interval, limit=100):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    r = requests.get(BINANCE_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return [float(candle[4]) for candle in data]


def calculate_upper_bb(closes):
    sma = statistics.mean(closes[-BB_PERIOD:])
    std = statistics.stdev(closes[-BB_PERIOD:])
    return sma + (BB_STD_DEV * std)


def check_pair(symbol, interval):
    closes = fetch_closes(symbol, interval)
    price = closes[-1]
    upper_bb = calculate_upper_bb(closes)

    print(f"{symbol} ({interval}) → Price: {price}, Upper BB: {upper_bb:.2f}")

    if price >= upper_bb:
        message = (
            f"🚨 BB ALERT\n"
            f"Pair: {symbol}\n"
            f"TF: {interval}\n"
            f"Price: {price}\n"
            f"Upper BB: {upper_bb:.2f}"
        )
        send_telegram(message)


def main():
    print("TEST ALERT: Bot is running correctly")
    for pair in PAIRS:
        check_pair(pair["symbol"], pair["interval"])


if __name__ == "__main__":
    main()
