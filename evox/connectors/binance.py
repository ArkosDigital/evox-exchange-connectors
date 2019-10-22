# coding=utf-8

'''
    Official Repository
    https://github.com/sammchardy/python-binance

    Official Documentation
    # Binance: https://binance-docs.github.io/apidocs/spot/en/
    # Python-Binance: https://python-binance.readthedocs.io/en/latest/
'''

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
from binance.exceptions import *


class BinanceMiddleware(object):
    '''
        Binance exchange management class

        Attributes
        ----------
        key : str
            The public key from Binance API account
        secret : str
            The secret key from Binance API account
    '''

    def __init__(self, key, secret):
        self._client = Client(api_key=key, api_secret=secret)
        self._websocketManager = BinanceSocketManager(self._client)
        self._conn_key = None

    @property
    def client(self):
        return self._client

    @property
    def socketManager(self):
        return self._websocketManager

    def msgHandler(self, msg):
        print(msg)

    def createLimitOrder(self, symbol, side, quantity, price):
        '''
            Post a new order for spot account.
            The type is limit and the time in force is GTC (good till canceled) by default.

            :param symbol: required
            :type symbol: str
            :param side: required
            :type side: str
            :param quantity: required
            :type quantity: decimal
            :param price: required
            :type price: str

            :returns: orderId, type integer
        '''
        orderType = ORDER_TYPE_LIMIT
        timeInForce = TIME_IN_FORCE_GTC

        try:
            side = SIDE_BUY if side.lower() == 'buy' else SIDE_SELL
        except AttributeError:
            raise('Error setting order side (buy or sell).')

        try:
            order = self.client.create_order(symbol=str(symbol),
                                             side=side,
                                             type=orderType,
                                             quantity=float(quantity),
                                             price=str(price),
                                             timeInForce=timeInForce)
            return order['orderId']

        except BinanceRequestException as error:
            print(f'Error creating limit order ({side}).')
            raise(error.message)
        except BinanceAPIException as error:
            print(f'Error creating limit order ({side}).')
            raise(error.message)
        except BinanceOrderMinAmountException as error:
            print(f'Error creating limit order ({side}).')
            raise(error.message)
        except BinanceOrderMinPriceException as error:
            print(f'Error creating limit order ({side}).')
            raise(error.message)
        except BinanceOrderMinTotalException as error:
            print(f'Error creating limit order ({side}).')
            raise(error.message)
        except BinanceOrderUnknownSymbolException as error:
            print(f'Error creating limit order ({side}).')
            raise(error.message)
        except BinanceOrderInactiveSymbolException as error:
            print(f'Error creating limit order ({side}).')
            raise(error.message)
        except BinanceOrderException as error:
            print(f'Error creating limit order ({side}).')
            raise(error.message)

    def createMarginOrder(self, symbol, side, quantity, price):
        '''
            Post a new order for margin account.
            The type is limit and the time in force is GTC (good till canceled) by default.

            :param symbol: required
            :type symbol: str
            :param side: required
            :type side: str
            :param quantity: required
            :type quantity: decimal
            :param price: required
            :type price: str

            :returns: orderId, type integer
        '''
        orderType = ORDER_TYPE_LIMIT
        timeInForce = TIME_IN_FORCE_GTC

        try:
            side = SIDE_BUY if side.lower() == 'buy' else SIDE_SELL
        except AttributeError:
            raise('Error setting order side (buy or sell).')

        try:
            order = self.client.create_margin_order(symbol=str(symbol),
                                                    side=side,
                                                    type=orderType,
                                                    quantity=float(quantity),
                                                    price=str(price),
                                                    timeInForce=timeInForce)
            return order['orderId']
        except BinanceAPIException as error:
            print(error.message)
            raise(f'Error creating margin order ({side}).')

    def fetchOHLCV(self, market, interval, limit=500):
        '''
            Kline/candlestick bars for a symbol.
            Klines are uniquely identified by their open time.
            OHLC means open, high, close and volume.

            :param symbol: required
            :type symbol: str
            :param interval: -
            :type interval: str
            :param limit: - Default 500; max 1000.
            :type limit: int

            :returns: list of lists or None if not found

            API Response Example
            ------
            [
                [
                    1499040000000,      # Open time
                    "0.01634790",       # Open
                    "0.80000000",       # High
                    "0.01575800",       # Low
                    "0.01577100",       # Close
                    "148976.11427815",  # Volume
                    1499644799999,      # Close time
                    "2434.19055334",    # Quote asset volume
                    308,                # Number of trades
                    "1756.87402397",    # Taker buy base asset volume
                    "28.46694368",      # Taker buy quote asset volume
                    "17928899.62484339" # Can be ignored
                ]
            ]
        '''
        interval = str(interval)
        if interval == '1m':
            interval = KLINE_INTERVAL_1MINUTE
        elif interval == '5m':
            interval = KLINE_INTERVAL_5MINUTE
        elif interval == '15m':
            interval = KLINE_INTERVAL_15MINUTE
        elif interval == '30m':
            interval = KLINE_INTERVAL_30MINUTE
        elif interval == '1h':
            interval = KLINE_INTERVAL_1HOUR
        elif interval == '4h':
            interval = KLINE_INTERVAL_4HOUR
        elif interval == '1d':
            interval = interval = KLINE_INTERVAL_1DAY
        elif interval == '1w':
            interval = KLINE_INTERVAL_1WEEK
        elif interval == '1M':
            interval = KLINE_INTERVAL_1MONTH
        else:
            print('Interval not implemented.')
            return None

        try:
            candles = self.client.get_klines(symbol=str(market),
                                             interval=str(interval),
                                             limit=int(limit))
        except BinanceAPIException as error:
            print('Error fetching candlesticks.')
            raise(error.message)
        except BinanceRequestException as error:
            print('Error fetching candlesticks.')
            raise(error.message)

        finally:
            if candles:
                return candles
            else:
                return None

    def fetchTicker(self):
        pass

    def fetchBalance(self, *args):
        '''
            Get current asset balance if have passed parameter or,
            if not, return each assets balances.

            :param asset: required
            :type asset: str

            :returns: list of dictionaries
        '''
        if args:
            asset = str(args[0])

            try:
                balanceAsset = self.client.get_asset_balance(asset=asset)
                return list(balanceAsset)

            except BinanceAPIException as error:
                print('Error fetching asset balance.')
                raise(error.message)

            except BinanceRequestException as error:
                print('Error fetching asset balance.')
                raise(error.message)
        else:
            try:
                balances = self.client.get_account()['balances']
                return balances

            except BinanceAPIException as error:
                print('Error fetching balances.')
                raise(error.message)

            except BinanceRequestException as error:
                print('Error fetching balances.')
                raise(error.message)
