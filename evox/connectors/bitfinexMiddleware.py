# coding=utf-8

'''
    Official Repository
    https://github.com/bitfinexcom/bitfinex-api-py

    Official Documentation
    # HTTP: https://github.com/bitfinexcom/bitfinex-api-py/blob/master/docs/rest_v2.md
    # Websockets: https://github.com/bitfinexcom/bitfinex-api-py/blob/master/docs/ws_v2.md
'''

import os
import sys
import asyncio
import time

# import bfxapi
from bfxapi import Client
from bfxapi.rest.bfx_rest import BfxRest


class BitfinexException(Exception):
    pass


class BitfinexMiddleware(object):
    '''
        Bitfinex exchange management class

        Attributes
        ------------
        key : str
            The public key from Bitfinex API account

        secret : str
            The secret key from Bitfinex API account
    '''

    def __init__(self, *args, **params):
        # self._client = BfxRest(API_KEY=params.get('api_key', None),
        #                        API_SECRET=params.get('api_secret', None))
        self._client = Client(API_KEY=params.get('api_key', None),
                              API_SECRET=params.get('api_secret', None)).rest

    @property
    def client(self):
        return self._client

    async def fetchOHLCV(self, market, interval='1D', limit=100, section='hist'):
        '''
            Available values: '1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '7D', '14D', '1M
            Kline/candlestick bars for a symbol.
            Klines are uniquely identified by their open time.
            OHLC means open, high, close and volume.
            1 day interval is default.

            :param symbol: required
            :type symbol: str
            :param interval: -
            :type interval: str
            :param limit: - Default 500; max 1000.
            :type limit: int

            :returns: list of lists or empty list if not found

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
            market = str(market).upper()
            market = f't{market}'
            candles = await self.client.get_public_candles(symbol=market,
                                                           section=section,
                                                           start='',
                                                           end='',
                                                           tf=interval,
                                                           limit=str(limit))

            return candles
        except:
            pass


if __name__ == '__main__':
    my_client = BitfinexMiddleware()

    async def run():
        candles = await my_client.fetchOHLCV(market='BTCUSD')
        print(type(candles))
        # print(len(candles))
        print(candles)

    t = asyncio.ensure_future(run())
    asyncio.get_event_loop().run_until_complete(t)
