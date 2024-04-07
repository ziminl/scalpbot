```import ccxt
import talib
import numpy as np
import time
import requests

exchange = ccxt.binance()

pairs = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT']

timeframe = '15m'

ma_period = 50
buy_threshold = 0.02
sell_threshold = 0.04
hodl_threshold = 0.01

discord_webhook_url = ''

def send_discord_alert(message):
    payload = {'content': message}
    try:
        response = requests.post(discord_webhook_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending Discord alert: {e}")

def fetch_price(pair):
    try:
        ohlcv = exchange.fetch_ohlcv(pair, timeframe)
        close_prices = np.array([candle[4] for candle in ohlcv])
        return close_prices
    except Exception as e:
        print(f"Error fetching data for {pair}: {e}")
        return None

def execute_buy(pair, price):
    message = f"Buying {pair} at {price}"
    send_discord_alert(message)

def execute_sell(pair, price):
    message = f"Selling {pair} at {price}"
    send_discord_alert(message)

def execute_stop_loss(pair, price):
    message = f"Stop loss triggered for {pair} at {price}"
    send_discord_alert(message)

while True:
    for pair in pairs:
        prices = fetch_price(pair)
        if prices is None:
            continue
        
        ma50 = talib.SMA(prices, timeperiod=ma_period)
        
        current_price = prices[-1]
        ma50_current = ma50[-1]
        
        buy_price = ma50_current * (1 - buy_threshold)
        sell_price = buy_price * (1 + sell_threshold)
        hodl_price = sell_price * (1 - hodl_threshold)
        
        trend_direction = 'uptrend' if ma50[-1] > ma50[-2] else 'downtrend'
        
        if current_price < buy_price and trend_direction == 'uptrend':
            execute_buy(pair, current_price)
        
        elif current_price > sell_price:
            execute_sell(pair, current_price)
        
        elif current_price < hodl_price:
            execute_sell(pair, current_price)
        
        elif current_price < buy_price * 0.99:
            execute_stop_loss(pair, current_price)
        
        time.sleep(60)
```
