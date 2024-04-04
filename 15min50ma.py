import ccxt
import time
import numpy as np

exchange = ccxt.binance({
    'enableRateLimit': True,
})

symbol = 'BTC/USDT'
timeframe = '15m'

ma_length = 50
tp_percentage = 0.02
sl_percentage = 0.01
entry_offset_percentage = 0.005

def get_15min_candles():
    candles = exchange.fetch_ohlcv(symbol, timeframe, limit=200)
    return np.array(candles)

def calculate_ma(candles):
    closes = candles[:, 4]
    ma = np.mean(closes[-ma_length:])
    return ma

def place_order(action, price):
    print(f"Placing {action} order at {price}.")

def main():
    while True:
        try:
            candles = get_15min_candles()
            ma = calculate_ma(candles)
            current_price = candles[-1, 4]

            if current_price < ma * 0.99:
                entry_price = ma * (1 + entry_offset_percentage)
                place_order("buy", entry_price)
                tp_price = entry_price * (1 + tp_percentage)
                sl_price = entry_price * (1 - sl_percentage)
                print(f"Entry Price: {entry_price}, TP: {tp_price}, SL: {sl_price}")

            time.sleep(20)

        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(20)

if __name__ == "__main__":
    main()


