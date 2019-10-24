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

    def __init__(self, **params):
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
            print(f'Error creating limit order ({side}).')
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
    orders = my_client.fetchOpenOrders()
    print(type(orders))
    print(len(orders))
    print(orders)