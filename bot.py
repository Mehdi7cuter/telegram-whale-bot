import requests
import asyncio
from telegram import Bot

# ====== تنظیمات ======
TELEGRAM_TOKEN = "8272662922:AAHbqIMSgqocZunv1aTdIXTLbatSYi_uaM0"
CHAT_ID = "8272662922"
COINGLASS_API_KEY = "7727c7f2149f47c89dd04f4102901cee"

SYMBOL_FILTER = "BTC"   # مثلا BTC
MIN_SIZE = 500000       # حداقل حجم دلار

bot = Bot(token=TELEGRAM_TOKEN)
sent_ids = set()

async def check_whales():
    url = "https://open-api-v4.coinglass.com/api/hyperliquid/whale-alert"
    headers = {
        "CG-API-KEY": COINGLASS_API_KEY
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if "data" not in data:
        return

    for trade in data["data"]:
        trade_id = trade.get("id")

        if trade_id in sent_ids:
            continue

        symbol = trade.get("symbol", "")
        side = trade.get("side", "")
        size = float(trade.get("size", 0))
        price = float(trade.get("price", 0))

        if SYMBOL_FILTER in symbol and size >= MIN_SIZE:
            message = f"""
🚨 Whale Alert 🚨

📊 Symbol: {symbol}
📈 Type: {side.upper()}
💰 Size: ${size:,.0f}
💵 Price: ${price}

🔥 Big Position Opened!
"""
            await bot.send_message(chat_id=CHAT_ID, text=message)
            sent_ids.add(trade_id)

async def main():
    while True:
        try:
            await check_whales()
        except Exception as e:
            print("Error:", e)

        await asyncio.sleep(30)

if __name__ == "main":
    asyncio.run(main())