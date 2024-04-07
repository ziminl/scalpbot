import time
import requests
from tradingview_ta import TA_Handler, Interval

discord_webhook_url = "https://discord.com/api/webhooks/1226437485563875439/-TvQw-s1H8xcjbvZh3nhe8s8tDDHryXrJEKHn_hDVhhbvHcjSsEKpAzEpeMvc2CGMJLg"

def send_discord_message(message):
    payload = {
        "content": message
    }
    requests.post(discord_webhook_url, json=payload)

def check_signals():
    handler = TA_Handler()
    handler.set_symbol_as("BTCUSD")
    handler.set_screener_as_crypto()
    handler.set_interval_as(Interval.INTERVAL_1_MINUTE)

    analysis = handler.get_analysis()

    if "STRONG_BUY" in analysis.summary or "BUY" in analysis.summary:
        send_discord_message(f"Buy signal detected! Current price: {analysis.indicators['close']}")
    elif "STRONG_SELL" in analysis.summary or "SELL" in analysis.summary:
        send_discord_message(f"Sell signal detected! Current price: {analysis.indicators['close']}")

if __name__ == "__main__":
    while True:
        check_signals()
        time.sleep(60)
