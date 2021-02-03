class Configuration:
    """
    parameter configuration
    """

    def __init__(self):
        self.base_return = 0.05
        self.base_trade_size = 10
        self.minimum_trade_size = 10
        self.time_interval = 86400
        self.tracing_pair = 'BTCUSDT'
        self.trading_pair = 'ETHUSDT'
        self.fee_pair = 'BNBUSDT'
