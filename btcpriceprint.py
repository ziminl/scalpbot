import ccxt

def get_btc_price(date_time):
    exchange = ccxt.binance()

    try:
        ticker = exchange.fetch_ohlcv('BTC/USDT', timeframe='1m', since=exchange.parse8601(date_time))

        if ticker:
            btc_price = ticker[-1][4]  # Closing price is the 5th element (index 4) in each ticker entry
            return btc_price
        else:
            return "ccxt error"
    except Exception as e:
        return f"Error: {str(e)}"

input_date_time = input("Enter YYYY-MM-DD HH:MM format: ")
btc_price = get_btc_price(input_date_time)
print(f"The price of Bitcoin on {input_date_time} was ${btc_price}" if isinstance(btc_price, float) else btc_price)
