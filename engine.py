import datetime as dt

import pandas as pd

from config import Configuration


class Engine:
    """
    trade strategy logic, determines trade side and sized for trade
    """

    def __init__(self):
        self.config = Configuration()
        self.trade_size = None
        self.side = None

    def previous_index_price(self, live_price):
        """
        updates csv (index_price_log) with the latest index price
        :return: the index price from when the function was last called
        """
        csv = 'index_price_log.csv'
        df = pd.read_csv(csv, index_col=0)
        try:
            old_index_price = df.iloc[0]['price']
        except:
            old_index_price = None
        datetime = dt.datetime.utcnow()
        top_row = pd.DataFrame({'datetime': [datetime], 'price': [live_price]})
        df = pd.concat([top_row, df]).reset_index(drop=True)
        df.to_csv(csv)
        return old_index_price

    def set_trade_parameters(self, live_price):
        """
        initialises attributes trade size and side ford dependent asset
        :return: True if trade parameters have been initialized and False if they haven't
        """
        self.trade_size = None
        prev_price = self.previous_index_price(live_price)
        if prev_price is None:
            return False
        real_return = (live_price - prev_price) / prev_price
        # print('{} ----- last {} minute(s) BTC return {}%'.format(dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M"), self.config.time_interval / 60,round(real_return * 100, 10)))
        real_trade_size = abs(round((real_return / self.config.base_return) * self.config.base_trade_size / 3.5) ** 2)
        if real_trade_size >= self.config.minimum_trade_size:
            self.trade_size = real_trade_size
            if real_return > 0:
                self.side = 'BUY'
            else:
                self.side = 'SELL'
            return True
        return False
