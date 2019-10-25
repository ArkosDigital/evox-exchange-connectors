# coding=utf-8

'''
    Official Documentation
    # HTTP: https://github.com/BitMEX/api-connectors/tree/master/official-http/python-swaggerpy
    # Websockets: https://github.com/BitMEX/api-connectors/tree/master/official-ws/python
'''

import bitmex

import json


class BitmexException(Exception):
    pass


class BitmexMiddleware(object):
    '''
        Bitmex exchange management class

        Attributes
        ------------
        key : str
            The public key from Bitmex API account

        secret : str
            The secret key from Bitmex API account
    '''
    ORDER_TYPE_LIMIT = 'Limit'
    ORDER_TYPE_MARKET = 'Market'

    SIDE_BUY = 'Buy'
    SIDE_SELL = 'Sell'

    KLINE_INTERVAL_1MINUTE = '1m'
    KLINE_INTERVAL_5MINUTE = '5m'
    KLINE_INTERVAL_1HOUR = '1h'
    KLINE_INTERVAL_1DAY = '1d'

    def __init__(self, *args, **params):
        self._client = bitmex.bitmex(test=params.get('test', False),
                                     api_key=params.get('api_key', None),
                                     api_secret=params.get('api_secret', None),
                                     config=None)

    @property
    def client(self):
        return self._client

    def createLimitOrder(self, symbol, side, quantity, price):
        '''
            Post a new order for your account.
            The type is limit and the time in force is GTC (good till canceled) by default.

            :param symbol: required
            :type symbol: str
            :param side: required
            :type side: str
            :param quantity: required
            :type quantity: integer
            :param price: required
            :type price: float

            :returns: orderId, type str
        '''
        try:
            side = self.SIDE_BUY if side.lower() == 'buy' else self.SIDE_SELL

            order = self.client.Order.Order_new(symbol=str(symbol),
                                                side=str(side),
                                                orderQty=abs(int(quantity)),
                                                price=float(price),
                                                ordType=self.ORDER_TYPE_LIMIT)
            return list(order.result())[0]['orderID']
        except AttributeError:
            raise BitmexException('Error setting order side (buy or sell).')
        except Exception as error:
            print(f'Error creating limit order ({side}).')
            raise BitmexException(error)

    def createMarketOrder(self, symbol, side, quantity):
        '''
            Post a new order of type market for your account.

            :param symbol: required
            :type symbol: str
            :param side: required
            :type side: str
            :param quantity: required
            :type quantity: integer

            :returns: orderId, type str
        '''
        try:
            side = self.SIDE_BUY if side.lower() == 'buy' else self.SIDE_SELL

            order = self.client.Order.Order_new(symbol=str(symbol),
                                                side=str(side),
                                                orderQty=abs(int(quantity)),
                                                ordType=self.ORDER_TYPE_MARKET)
            return list(order.result())[0]['orderID']
        except AttributeError:
            raise BitmexException('Error setting order side (buy or sell).')
        except Exception as error:
            print(f'Error creating market order ({side}).')
            raise BitmexException(error)

    def fetchOHLCV(self, market, interval='1d', limit=100, reverse=True):
        '''
            Kline/candlestick bars for a symbol.
            Klines are uniquely identified by their open time.
            OHLC means open, high, close and volume.
            1 day interval is default.
            Available options: [1m,5m,1h,1d].

            :param symbol: required
            :type symbol: str
            :param interval: -
            :type interval: str
            :param limit: - Default 100; max 1000.
            :type limit: int
            :param reverse: - Default True.
            :type reverse: boolean

            :returns: list of dictonaries or [] if not found

            API Response Example
            --------
            [
                {
                    "timestamp": "2019-10-24T20:44:08.362Z",
                    "symbol": "string",
                    "open": 0,
                    "high": 0,
                    "low": 0,
                    "close": 0,
                    "trades": 0,
                    "volume": 0,
                    "vwap": 0,
                    "lastSize": 0,
                    "turnover": 0,
                    "homeNotional": 0,
                    "foreignNotional": 0
                }
            ]
        '''
        try:
            interval = str(interval)
            if interval == '1m':
                interval = self.KLINE_INTERVAL_1MINUTE
            elif interval == '5m':
                interval = self.KLINE_INTERVAL_5MINUTE
            elif interval == '1h':
                interval = self.KLINE_INTERVAL_1HOUR
            elif interval == '1d':
                interval = self.KLINE_INTERVAL_1DAY
            else:
                print('Interval not implemented.')
                return []
            
            candles = self.client.Trade.Trade_getBucketed(binSize=str(interval),
                                                          symbol=str(market),
                                                          count=int(limit),
                                                          reverse=bool(reverse))

            return candles.result()[0]

        except Exception as error:
            print('Error fetching candlesticks (OHLCV).')
            raise BitmexException(error)

    def fetchTicker(self, symbol):
        '''
            It just returns the last candle in timeframe
            of 1 day like fetchOHCLV method.
            Must be reviewed!
            --------
        '''
        try:
            # return self.client.Quote.Quote_get(symbol='XBT')
            return self.fetchOHLCV(market=symbol, limit=1)
        except Exception as error:
            print('Error fetching ticker.')
            raise BitmexException(error)

    def fetchBalance(self, currency='XBt'):
        '''
            Get current asset balance if have passed parameter or,
            if not, return each assets balances. XBt by default.

            :param asset: -
            :type asset: str

            :returns: dictionary with API response

            API Response Example
            --------
            {
                "account": 0,
                "currency": "string",
                "prevDeposited": 0,
                "prevWithdrawn": 0,
                "prevTransferIn": 0,
                "prevTransferOut": 0,
                "prevAmount": 0,
                "prevTimestamp": "2019-10-24T12:17:45.777Z",
                "deltaDeposited": 0,
                "deltaWithdrawn": 0,
                "deltaTransferIn": 0,
                "deltaTransferOut": 0,
                "deltaAmount": 0,
                "deposited": 0,
                "withdrawn": 0,
                "transferIn": 0,
                "transferOut": 0,
                "amount": 0,
                "pendingCredit": 0,
                "pendingDebit": 0,
                "confirmedDebit": 0,
                "timestamp": "2019-10-24T12:17:45.777Z",
                "addr": "string",
                "script": "string",
                "withdrawalLock": [
                    "string"
                ]
            }
        '''
        try:
            balance = self.client.User.User_getWallet(currency=currency)
            return balance.result()[0]
        except Exception as error:
            print(f'Error fetching asset balance.')
            raise BitmexException(error)

    def fetchOrders(self, *args):
        '''
            Fetch all orders (new, filled, cancelled) on a symbol,
            buy and sell orders.
            If the symbol is not sent, orders for all symbols
            will be returned in an array.

            :param symbol: -
            :type symbol: str

            :returns: list of dictionaries with API response
        '''
        try:
            if args:
                symbol = args[0]
                orders = self.client.Order.Order_getOrders(symbol=symbol)
            else:
                orders = self.client.Order.Order_getOrders()

            return orders.result()[0]

        except Exception as error:
            print(f'Error fetching all orders.')
            raise BitmexException(error)

    def fetchOpenOrders(self, *args):
        '''
            Fetch all open orders on a symbol, buy and sell orders.
            If the symbol is not sent, orders for all symbols
            will be returned in an array.

            :param symbol: -
            :type symbol: str

            :returns: list of dictionaries with API response
        '''
        try:
            filters = json.dumps({'open': True})

            if args:
                symbol = args[0]
                orders = self.client.Order.Order_getOrders(symbol=symbol,
                                                           filter=filters)
            else:
                orders = self.client.Order.Order_getOrders(filter=filters)

            return orders.result()[0]

        except Exception as error:
            print(f'Error fetching all orders.')
            raise BitmexException(error)

    def fetchOpenBuyOrders(self, *args):
        '''
            Fetch all buy orders on a symbol,
            If the symbol is not sent, buy open orders for all
            symbols will be returned in an array.

            :param symbol: -
            :type symbol: str

            :returns: list of dictionaries with API response
        '''
        try:
            if args:
                symbol = str(args[0])
                buys = self.fetchOpenOrders(symbol)
            else:
                buys = self.fetchOpenOrders()

            buys = [buy for buy in buys
                    if buy['side'].lower() == self.SIDE_BUY.lower()]
            return buys

        except Exception as error:
            print('Error fetching open buy orders.')
            raise BitmexException(error)

    def fetchOpenSellOrders(self, *args):
        '''
            Fetch all sell orders on a symbol,
            If the symbol is not sent, sell open orders for all
            symbols will be returned in an array.

            :param symbol: -
            :type symbol: str

            :returns: list of dictionaries with API response
        '''
        try:
            if args:
                symbol = str(args[0])
                sells = self.fetchOpenOrders(symbol)
            else:
                sells = self.fetchOpenOrders()

            sells = [sell for sell in sells
                     if sell['side'].lower() == self.SIDE_SELL.lower()]
            return sells

        except Exception as error:
            print('Error fetching open sell orders.')
            raise Exception(error)


if __name__ == '__main__':
    key = 'G05-RxwEt6Wl8n2khC-nvuJf'
    secret = '7yw2poyvsEoDjjoGfsQd-JQlGpVE7wwv2vg9swzmpGMRH36t'
    my_client = BitmexMiddleware(test=True,
                                 api_key=key,
                                 api_secret=secret)
    # order = my_client.createMarketOrder(symbol='ETHUSD',
    #                                    side='sell',
    #                                    quantity=1)
    # print(type(order))
    # print(order)
    # balance = my_client.fetchOHLCV(market='XBT', interval='1M', limit=1000)
    balance = my_client.fetchTicker(symbol='XBT')
    print(type(balance))
    print(len(balance))
    print(balance)
