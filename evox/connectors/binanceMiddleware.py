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
        ------------
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
            raise AttributeError('Error setting order side (buy or sell).')

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
            raise BaseException(error.message)
        except BinanceAPIException as error:
            print(f'Error creating limit order ({side}).')
            raise BaseException(error.message)
        except BinanceOrderMinAmountException as error:
            print(f'Error creating limit order ({side}).')
            raise BaseException(error.message)
        except BinanceOrderMinPriceException as error:
            print(f'Error creating limit order ({side}).')
            raise BaseException(error.message)
        except BinanceOrderMinTotalException as error:
            print(f'Error creating limit order ({side}).')
            raise BaseException(error.message)
        except BinanceOrderUnknownSymbolException as error:
            print(f'Error creating limit order ({side}).')
            raise BaseException(error.message)
        except BinanceOrderInactiveSymbolException as error:
            print(f'Error creating limit order ({side}).')
            raise BaseException(error.message)
        except BinanceOrderException as error:
            print(f'Error creating limit order ({side}).')
            raise BaseException(error.message)

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
            raise BaseException('Error setting order side (buy or sell).')

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
            raise BaseException(f'Error creating margin order ({side}).')

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
            --------
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
        try:
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

            candles = self.client.get_klines(symbol=str(market),
                                             interval=str(interval),
                                             limit=int(limit))

            return candles

        except BinanceAPIException as error:
            print('Error fetching candlesticks.')
            raise BaseException(error.message)
        except BinanceRequestException as error:
            print('Error fetching candlesticks.')
            raise BaseException(error.message)

    def fetchTicker(self, symbol):
        '''
            Fetch latest ticker data by trading symbol.
            24 hours price change statistics.

            :param symbol: required
            :type symbol: str

            :returns: dictionary with API response

            API Response Example
            --------
            {
                "symbol": "BNBBTC",
                "priceChange": "-94.99999800",
                "priceChangePercent": "-95.960",
                "weightedAvgPrice": "0.29628482",
                "prevClosePrice": "0.10002000",
                "lastPrice": "4.00000200",
                "lastQty": "200.00000000",
                "bidPrice": "4.00000000",
                "askPrice": "4.00000200",
                "openPrice": "99.00000000",
                "highPrice": "100.00000000",
                "lowPrice": "0.10000000",
                "volume": "8913.30000000",
                "quoteVolume": "15.30000000",
                "openTime": 1499783499040,
                "closeTime": 1499869899040,
                "firstId": 28385,   // First tradeId
                "lastId": 28460,    // Last tradeId
                "count": 76         // Trade count
            }
        '''
        try:
            symbol = str(symbol)
            return self.client.get_ticker(symbol=symbol)

        except BinanceAPIException as error:
            print('Error fetching ticker.')
            raise BaseException(error.message)

        except BinanceRequestException as error:
            print('Error fetching ticker.')
            raise BaseException(error.message)

    def fetchBalance(self, *args):
        '''
            Get current asset balance if have passed parameter or,
            if not, return each assets balances.

            :param asset: required
            :type asset: str

            :returns: list of dictionaries

            API Response Example
            --------
            [
                {
                    "asset": "BTC",
                    "free": "4723846.89208129",
                    "locked": "0.00000000"
                }
            ]
        '''
        try:
            if args:
                asset = str(args[0])

                balanceAsset = self.client.get_asset_balance(asset=asset)
                return list(balanceAsset)
            else:
                balances = self.client.get_account()['balances']
                return balances

        except BinanceAPIException as error:
            print('Error fetching asset balance.')
            raise BaseException(error.message)

        except BinanceRequestException as error:
            print('Error fetching asset balance.')
            raise BaseException(error.message)

    def fetchOpenOrders(self, *args):
        '''
            Fetch all open orders on a symbol,
            buy and sell orders. If the symbol is not sent,
            orders for all symbols will be returned in an array.

            :param symbol: -
            :type symbol: str

            :returns: dictionary with API response

            API Response Example
            --------
            [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "orderListId": -1, //Unless OCO, the value will always be -1
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "cummulativeQuoteQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559,
                    "updateTime": 1499827319559,
                    "isWorking": true
                }
                ...
            ]
        '''
        try:
            if args:
                symbol = str(args[0])
                return self.client.get_open_orders(symbol=symbol)
            else:
                return self.client.get_open_orders()

        except BinanceAPIException as error:
            print('Error fetching all open orders.')
            raise BaseException(error.message)

        except BinanceRequestException as error:
            print('Error fetching all open orders.')
            raise BaseException(error.message)

    def fetchOpenBuyOrders(self, *args):
        '''
            Fetch all open buy orders on a symbol,
            If the symbol is not sent, buy orders for all
            symbols will be returned in an array.

            :param symbol: -
            :type symbol: str

            :returns: dictionary with API response

            API Response Example
            --------
            [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "orderListId": -1, //Unless OCO, the value will always be -1
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "cummulativeQuoteQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559,
                    "updateTime": 1499827319559,
                    "isWorking": true
                }
            ]
        '''
        try:
            if args:
                symbol = str(args[0])
                buys = self.fetchOpenOrders(symbol)
            else:
                buys = self.fetchOpenOrders()

            buys = [buy for buy in buys
                    if buy['side'].lower() == "BUY".lower()]
            return buys

        except Exception as error:
            print('Error fetching open buy orders.')
            raise Exception(error)

    def fetchOpenSellOrders(self, *args):
        '''
            Fetch all sell buy orders on a symbol,
            If the symbol is not sent, buy orders for all
            symbols will be returned in an array.

            :param symbol: -
            :type symbol: str

            :returns: dictionary with API response

            API Response Example
            --------
            [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "orderListId": -1, //Unless OCO, the value will always be -1
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "cummulativeQuoteQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "SELL",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559,
                    "updateTime": 1499827319559,
                    "isWorking": true
                }
            ]
        '''
        try:
            if args:
                symbol = str(args[0])
                sells = self.fetchOpenOrders(symbol)
            else:
                sells = self.fetchOpenOrders()

            sells = [sell for sell in sells
                     if sell['side'].lower() == "SELL".lower()]
            return sells

        except Exception as error:
            print('Error fetching open sell orders.')
            raise Exception(error)


if __name__ == '__main__':
    my_client = BinanceMiddleware('', '')
    klines = my_client.fetchOHLCV(market='BTCUSDT', interval='1', limit=100)
    # print(len(klines))
