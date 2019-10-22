from abc import ABCMeta, abstractmethod


class BaseExchangeInterface(metaclass=ABCMeta):
    '''
    Interface
    '''

    # --- Public Methods

    @abstractmethod
    def fetchMarkets(self):
        """
            Describe
            ----------
            Parameters
        """
        pass

    @abstractmethod
    def fetchCurrencies(self):
        """
            Describe
            ----------
            Parameters
        """
        pass

    @abstractmethod
    def fetchTicker(self):
        """
            Describe
            ----------
            Parameters
        """
        pass

    @abstractmethod
    def fetchOrderBook(self):
        """
            Describe
            ----------
            Parameters
        """
        pass

    @abstractmethod
    def fetchTrades(self):
        """
            Describe
            ----------
            Parameters
        """
        pass

    @abstractmethod
    def fetchOHLCV(self):
        """
            fetchOHLCV
            ----------
            A list of candles or kline data for traded volumes in different timeframes 1m, 15m, 1h, 1d, ... + OHLCV structure

            Parameters
            ----------
            symbol,
            timeframe,
            since,
            limit

        """
        pass

    # --- Private Methods

    @abstractmethod
    def fetchBalance(self):
        """
            Get the amount of funds available for trading or funds locked in orders

            Parameters
            ----------
        """
        pass

    @abstractmethod
    def createOrder(self):
        """
            Limit/market orders + order structure

            Parameters
            ----------
        """
        pass

    @abstractmethod
    def cancelOrder(self):
        """
            Cancel an order

            Parameters
            ----------
        """
        pass

    @abstractmethod
    def cancelAllOrders(self):
        """
            Cancel all open orders (buy or sells)

            Parameters
            ----------
        """
        pass

    @abstractmethod
    def fetchOpenOrders(self):
        """
            A list of all open orders

            Parameters
            ----------
        """
        pass

    @abstractmethod
    def fetchAllOrders(self):
        """
            A list of all orders

            Parameters
            ----------
        """
        pass

    @abstractmethod
    def fetchMyTrades(self):
        """
            The personal history of filled trades for the account + trade structure

            Parameters
            ----------
        """
        pass
