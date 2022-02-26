# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IStrategy, IntParameter)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


# This class is a sample. Feel free to customize it.
class BBRSIOPT(IStrategy):
    """
    This is a sample strategy to inspire you.
    More information in https://www.freqtrade.io/en/latest/strategy-customization/

    You can:
        :return: a Dataframe with all mandatory indicators for the strategies
    - Rename the class name (Do not forget to update class_name)
    - Add any methods you want to build your strategy
    - Add any lib you need to build your strategy

    You must keep:
    - the lib in the section "Do not remove these libs"
    - the methods: populate_indicators, populate_buy_trend, populate_sell_trend
    You should keep:
    - timeframe, minimal_roi, stoploss, trailing_*
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "0": 100
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.99

    # Trailing stoploss
    trailing_stop = False
    # trailing_only_offset_is_reached = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0  # Disabled / not configured

    # Hyperoptable parameters
    buy_rsi = IntParameter(low=1, high=50, default=25, space='buy', optimize=True, load=True)
    sell_rsi = IntParameter(low=50, high=100, default=75, space='sell', optimize=True, load=True)
    buy_bb = CategoricalParameter(["bb_l05","bb_l1","bb_l15","bb_l2","bb_l25","bb_l3","bb_m"], default="bb_l2", space='buy', optimize=True, load=True)
    sell_bb = CategoricalParameter(["bb_m","bb_l05","bb_l1","bb_u05","bb_u1","bb_u15","bb_u2","bb_u25","bb_u3",], default='bb_m1', space='sell', optimize=True, load=True)
    buy_rsi_enabled = CategoricalParameter([True, False], default=True, space='buy', optimize=True, load=True)
    sell_rsi_enabled = CategoricalParameter([True, False], default=True, space='sell', optimize=True, load=True)


    # Optimal timeframe for the strategy.
    timeframe = '1h'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = True

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    # Optional order type mapping.
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc'
    }

    plot_config = {
        'main_plot': {
            'tema': {},
            'sar': {'color': 'white'},
        },
        'subplots': {
            "MACD": {
                'macd': {'color': 'blue'},
                'macdsignal': {'color': 'orange'},
            },
            "RSI": {
                'rsi': {'color': 'red'},
            }
        }
    }

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
        """

        # Momentum Indicators
        # ------------------------------------


        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)

        # Overlap Studies
        # ------------------------------------

        # Bollinger Bands
        bollinger05 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=0.5)
        dataframe['bb_l05'] = bollinger05['lower']
        #dataframe['bb_m05'] = bollinger05'mid']
        dataframe['bb_u05'] = bollinger05['upper']

        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=1)
        dataframe['bb_l1'] = bollinger['lower']
        #dataframe['bb_m1'] = bollinger['mid']
        dataframe['bb_u1'] = bollinger['upper']

        bollinger15 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=1.5)
        dataframe['bb_l15'] = bollinger15['lower']
        #dataframe['bb_m15'] = bollinger15['mid']
        dataframe['bb_u15'] = bollinger15['upper']

        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_l2'] = bollinger2['lower']
        dataframe['bb_m'] = bollinger2['mid']
        dataframe['bb_u2'] = bollinger2['upper']

        bollinger25 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2.5)
        dataframe['bb_l25'] = bollinger25['lower']
        #dataframe['bb_m25'] = bollinger25['mid']
        dataframe['bb_u25'] = bollinger25['upper']

        bollinger3 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=3)
        dataframe['bb_l3'] = bollinger3['lower']
        #dataframe['bb_m3'] = bollinger3['mid']
        dataframe['bb_u3'] = bollinger3['upper']




        # Bollinger Bands - Weighted (EMA based instead of SMA)
        # weighted_bollinger = qtpylib.weighted_bollinger_bands(
        #     qtpylib.typical_price(dataframe), window=20, stds=2
        # )

        # Retrieve best bid and best ask from the orderbook
        # ------------------------------------
        """
        # first check if dataprovider is available
        if self.dp:
            if self.dp.runmode.value in ('live', 'dry_run'):
                ob = self.dp.orderbook(metadata['pair'], 1)
                dataframe['best_bid'] = ob['bids'][0][0]
                dataframe['best_ask'] = ob['asks'][0][0]
        """

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        buy_rsi_l = 0
        if self.buy_rsi_enabled.value:
            buy_rsi_l = self.buy_rsi.value

        dataframe.loc[
            (
                (dataframe['rsi'] > buy_rsi_l)&
                (dataframe["close"] < dataframe[self.buy_bb.value])

            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with sell column
        """
        sell_rsi_l = 0
        if self.sell_rsi_enabled.value:
            sell_rsi_l = self.sell_rsi.value

        dataframe.loc[
            (
                (dataframe['rsi'] > sell_rsi_l)&
                (dataframe["close"] > dataframe[self.sell_bb.value])
            ),
            'sell'] = 1
        return dataframe
