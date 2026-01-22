import os
import requests
from binance.client import Client

# ========== ENV VARIABLES ==========
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ========== BINANCE CLIENT ==========
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# ========== TELEGRAM ==========
def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)


# ========== PRICE FETCH ==========
def get_latest_price(symbol: str, interval: str):
    klines = client.get_klines(
        symbol=symbol,
        interval=interval,
        limit=2
    )

    last_closed_candle = klines[-2]
    close_price = float(last_closed_candle[4])

    return close_price


# ========== MAIN ==========
def main():
    btc_price = get_latest_price("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE)
    sol_price = get_latest_price("SOLUSDT", Client.KLINE_INTERVAL_30MINUTE)

    message = (
        "📊 Crypto Price Update\n\n"
        f"🟡 BTC (15m): ${btc_price}\n"
        f"🟣 SOL (30m): ${sol_price}"
    )

    send_telegram(message)


if __name__ == "__main__":
    main()
