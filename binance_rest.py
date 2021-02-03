import hashlib
import hmac
import time
from urllib.parse import urljoin, urlencode

import requests

import config
import performance as per
from engine import Engine


class Binance:
    def __init__(self):
        self.c = config.Configuration()
        keyFile = open('api_credentials.txt', 'r')
        self.key = keyFile.readline().rstrip()
        self.secret = keyFile.readline().rstrip()
        self.base_url = 'https://api.binance.com'
        self.trade_engine = Engine()
        self.performance = per.Performance()

    def api_connector(self, path, params, secret=False, get = True):
        url = urljoin(self.base_url, path)
        if secret:
            query_string = urlencode(params)
            params['signature'] = hmac.new(self.secret.encode('utf-8'), query_string.encode('utf-8'),
                                           hashlib.sha256).hexdigest()
            headers = {'X-MBX-APIKEY': self.key}
            if get:
                r = requests.get(url, headers=headers, params=params)
            else:
                r = requests.post(url, headers=headers, params=params)
        else:
            r = requests.get(url, params=params)
        if r.status_code == 200:
            data = r.json()
            return data
        else:
            raise self.BinanceException(status_code=r.status_code, data=r.json())

    def get_balances(self):
        path = '/api/v3/account'
        timestamp = int(time.time() * 1000)
        params = {'timestamp': timestamp}
        data = self.api_connector(path, params, True)
        for i in data['balances']:
            if (i['asset']) == 'USDT':
                usdt_balance = i['free']  # does locked include open orders??
            if (i['asset']) == 'LTC':
                ltc_balance = i['free']
        return (usdt_balance,ltc_balance)

    def get_price(self, pair, avg=True):
        if avg:
            path = '/api/v3/avgPrice'
        else:
            path = '/api/v3/ticker/price'
        params = {'symbol': pair}
        data = self.api_connector(path, params)
        price = float(data['price'])
        return price

    def execute_trade(self):
        parameters_set = self.trade_engine.set_trade_parameters(self.get_price(self.c.tracing_pair))
        if parameters_set:
            path = '/api/v3/order'
            timestamp = int(time.time() * 1000)
            params = {
                'symbol': self.c.trading_pair,
                'side': self.trade_engine.side,
                'type': 'MARKET',
                'quoteOrderQty': self.trade_engine.trade_size,
                'timestamp': timestamp
            }
            data = self.api_connector(path, params, True, False)
            self.performance.record(data)

    class BinanceException(Exception):
        def __init__(self, status_code, data):
            self.status_code = status_code
            if data:
                self.code = data['code']
                self.msg = data['msg']
            else:
                self.code = None
                self.msg = None
            message = f"{status_code} [{self.code}] {self.msg}"
            super().__init__(message)

