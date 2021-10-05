from binance.enums import *
from binance.client import Client
import pandas as pd
import json
import datetime

'''
I've decided to use the binance API to get historical data. ref:
    https://python-binance.readthedocs.io/en/latest/binance.html
Unfortunately, the API requires my personal key and with it anyone
can buy/sell crypto on my account. Hence, the code is given without
the key and will not run. Along with the code I provide the csv file "stocks.csv"
which contains the result of running the code with the given settings
'''


API_KEY = 'insert_your_key'
SECRET_KEY = 'insert_your_secret_key'

client = Client(API_KEY, SECRET_KEY)

def get_klines(coin, interval, start, end=None)->[]:
    """Get klines of a cript and returns OHLCV values (i.e.  Open, High, Low, Close and Volume).

    Args:
        coin (str)
        interval (binance.enum): binance enum (https://python-binance.readthedocs.io/en/latest/binance.html?highlight=binance.enum#module-binance.client).
                                Example KLINE_INTERVAL_1HOUR,   KLINE_INTERVAL_1MONTH
        start (str|int):  Start date string in UTC format or timestamp in milliseconds
        end (str|int, optional): End date string in UTC format or timestamp in milliseconds. Defaults to None.
    Returns:
        [int]: Array of OHLCV values for the given start|end time and interval
    """    
    klines = client.get_historical_klines(coin, interval, start_str=start, end_str=end)
    # convert to pandas 
    df = pd.read_json(json.dumps(klines, indent=4, sort_keys=True))
    df = df[df.columns[1:5]]
    # rename columns with correct names
    df = df.rename(columns={ 1: "Open", 2: "High", 3: "Low", 4: "Close"})
    return df


coins = ['BTC', 'ETH', 'UNI', 'ADA', 'BNB', 'CAKE', 'XMR']
# coins = ['BTC', 'ETH', 'ADA', 'BNB', 'XMR'] # no defi

def generate_dataset(coins):
    frames = []
    for c in coins:
        coin_str = c+'BUSD' # BUSD = stable coin with dollar
        interval = KLINE_INTERVAL_1HOUR
        # interval = KLINE_INTERVAL_15MINUTE
        coin_data = get_klines(coin_str, interval, '2021-01-1', end='2021-6-21')
        coin_price = coin_data['Close'].rename(c)
        # coin_price.rename(columns={'Close': c})
        
        frames.append(coin_price)
        
    stocks = pd.concat(frames, axis=1)
    return stocks

stocks =  generate_dataset(coins)
# stocks.to_csv('./stocks.csv', index=False)