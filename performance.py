import datetime as dt

import pandas as pd

import binance_rest
import config


class Performance:
    """
    records performance of trading bot
    """

    def __init__(self):
        self.total_buy_qty = 0
        self.quote_buy_qty = 0
        self.total_sell_qty = 0
        self.quote_sell_qty = 0
        self.total_fees = 0
        self.csv = 'tracing_performance.csv'
        self.c = config.Configuration()

    def record(self, data):
        brest = binance_rest.Binance()
        fees = 0
        price = 0
        for f in data['fills']:
            fees += float(f['commission'])
            price += float(f['price'])*float(f['qty'])
        side = data['side']
        qty = float(data['executedQty'])
        avg_price = price/qty
        quote_qty = float(data['cummulativeQuoteQty'])
        trade_df = pd.DataFrame({'side':[side],'qty':[qty],'quote_qty':[quote_qty],'avg_price':[avg_price]})
        trade_df = trade_df.round(2)


        if side == 'BUY':
            self.total_buy_qty += qty
            self.quote_buy_qty += quote_qty
        else:
            self.total_sell_qty += qty
            self.quote_sell_qty += quote_qty
        self.total_fees += fees
        try:
            avg_buy = self.quote_buy_qty / self.total_buy_qty
        except:
            avg_buy = 0
        try:
            avg_sell = self.quote_sell_qty / self.total_sell_qty
        except:
            avg_sell = 0
        avg_profit = avg_sell - avg_buy
        avg_fees_usd = (self.total_fees / (self.total_buy_qty + self.total_sell_qty))*0.8 * brest.get_price(self.c.fee_pair, False)
        if self.total_sell_qty < self.total_buy_qty:
            cycled_volume = self.total_sell_qty
        else:
            cycled_volume = self.total_buy_qty
        trading_profit = avg_profit * cycled_volume
        total_fees = avg_fees_usd * (self.total_sell_qty + self.total_buy_qty)
        real_profit = trading_profit - avg_fees_usd * total_fees
        account_balances = brest.get_balances()
        usdt_balance = float(account_balances[0])
        ltc_balance = float(account_balances[1])
        account_usdt_value = usdt_balance + ltc_balance * brest.get_price(self.c.trading_pair, False)

        per_df = pd.DataFrame(
            {'avg sell': [avg_sell], 'avg buy': [avg_buy], 'avg profit': [avg_profit], 'cycled ltc volume': [cycled_volume],
             'usdt balance':[usdt_balance], 'ltc balance':[ltc_balance], 'account usdt value': [account_usdt_value],
             'trading profit': [trading_profit], 'real profit': [real_profit]})
        per_df = per_df.round(2)
        per_df.to_csv(self.csv)
        print('\n{}\n-----TRADE-----\n{}\n---------------\n\nPerformance\n{}\n\n'.format(
            dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M"),trade_df,per_df))