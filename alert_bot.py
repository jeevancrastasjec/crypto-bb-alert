import requests
import statistics
import time

BINANCE_URL = "https://data-api.binance.vision/api/v3/klines"

# CONFIG
PAIRS = [
    {"symbol": "BTCUSDT", "interval": "15m"},
    {"symbol": "SOLUSDT", "interval": "30m"}
]

BB_PERIOD = 20
BB_STD_DEV = 2


def fetch_closes(symbol, interval, limit=100):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(BINANCE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    closes = [float(candle[4]) for candle in data]
    return closes


def calculate_bollinger_bands(closes):
    sma = statistics.mean(closes[-BB_PERIOD:])
    std = statistics.stdev(closes[-BB_PERIOD:])
    upper_band = sma + (BB_STD_DEV * std)
    lower_band = sma - (BB_STD_DEV * std)
    return sma, upper_band, lower_band


def check_pair(symbol, interval):
    closes = fetch_closes(symbol, interval)
    last_price = closes[-1]

    sma, upper, lower = calculate_bollinger_bands(closes)

    print(f"\n{symbol} | TF: {interval}")
    print(f"Price: {last_price}")
    print(f"Upper BB: {upper:.2f}")

    if last_price >= upper:
        print(f"🚨 ALERT: {symbol} touching UPPER Bollinger Band!")
    else:
        print("✅ No alert")


def main():
    print("TEST ALERT: Bot is running correctly")
    for pair in PAIRS:
        check_pair(pair["symbol"], pair["interval"])


if __name__ == "__main__":
    main()
