import os
import requests
from datetime import datetime

# ========================
# TELEGRAM CONFIG
# ========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram credentials missing")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("❌ Telegram error:", response.text)
    else:
        print("📨 Telegram sent")


# ========================
# BINANCE (PUBLIC API)
# ========================
def get_price(symbol):
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": symbol}

    r = requests.get(url, params=params)
    r.raise_for_status()

    return float(r.json()["price"])


# ========================
# MAIN LOGIC
# ========================
def main():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # BTC 15m
    btc_price = get_price("BTCUSDT")
    send_telegram(
        f"🟠 BTC Update (15m)\n"
        f"Price: ${btc_price:,.2f}\n"
        f"Time: {now}"
    )

    # SOL 30m
    sol_price = get_price("SOLUSDT")
    send_telegram(
        f"🟣 SOL Update (30m)\n"
        f"Price: ${sol_price:,.2f}\n"
        f"Time: {now}"
    )

    print("✅ Run completed successfully")


if __name__ == "__main__":
    main()
