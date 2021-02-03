import datetime as dt
import time

import pandas as pd

import config
from binance_rest import Binance


class RunStrategy:
    def __init__(self):
        b = Binance()
        c = config.Configuration()
        df = pd.DataFrame(columns=('datetime', 'price'))
        df.to_csv('index_price_log.csv')
        print('index log initialized')
        count = 0
        while True:
            try:
                b.execute_trade()
            except Exception as e:
                print('_______ERROR_______\n',e)
            count += 1
            if count == 10:
                print(dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M"),'   ETH price:',b.get_price(c.trading_pair,False))
                count = 0
            time.sleep(c.time_interval)


RunStrategy()
