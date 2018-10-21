import src.fuzzy as fuzzy
from src.generator import Generator
from datetime import datetime as dt
import math
import pandas as pd

BROKERAGE_RATE = 0.2
BROKERAGE_MIN_FEE = 30
FIRST_INDICATOR_INDEX = 5  # DateTime is the index and is not counted as the column


class Evaluator:

    def __init__(self, data, generator=None):
        data_indicator = data.iloc[:, range(FIRST_INDICATOR_INDEX, len(data.columns), 1)]
        if generator is None:
            self._generator = Generator(data_indicator)
        else:
            self._generator = generator
        self._data = data

    @property
    def generator(self):
        return self._generator

    def calcBrokerage(self, volume, price):
        if volume == 0 or price == 0:
            return 0

        fee = round(volume * price * BROKERAGE_RATE / 100, 2)
        return fee

    # Execute trade and return Long position, Short Position.
    # Update and return new Short Price if there is short instrument executed.
    def execute(self, data, balance, longPos, shortPos):
        assert (balance >= 0)
        assert (longPos * shortPos == 0)  # at least on of longPos and shortPos is 0

        buy_price = data['High']  # the price for buy is at High
        sell_price = data['Low']  # the price for sell is at Low
        asset = round(balance + longPos * sell_price - shortPos * buy_price, 2)
        if asset <= 0:
            return balance, longPos, shortPos, asset

        signal = data['Signal']  # the strength of the operation
        # print("Signal", signal, "High", buy_price, "Low", sell_price)
        if signal > 0:
            if longPos > 0:
                # same direction should use lower value (i.e. balance) to restore the position
                valueToLong = balance * signal
            else:
                # opposite direction should use larger value (i.e. balance) to restore the position
                # if (shortPos == 0) then (asset == balance)
                valueToLong = balance * signal

            posToBuy = math.floor(valueToLong / buy_price)
            if self.calcBrokerage(posToBuy, buy_price) <= BROKERAGE_MIN_FEE:
                # if the volume is too small, do not execute
                return balance, longPos, shortPos, asset

            if posToBuy == 0:
                pass
            elif shortPos > posToBuy:
                # longPos is 0 here, reduce the shortPos
                shortPos -= posToBuy
                balance -= posToBuy * buy_price + self.calcBrokerage(posToBuy, buy_price)
            else:
                # extra longPos is needed, clear all the shortPos
                deltaPos = posToBuy - shortPos
                longPos += deltaPos
                balance -= posToBuy * buy_price + self.calcBrokerage(shortPos, buy_price) \
                           + self.calcBrokerage(deltaPos, buy_price)
                shortPos = 0

        elif signal < 0:
            if shortPos > 0:
                # same direction should use lower value (i.e. asset) to restore the position
                valueToShort = asset * (signal * -1)
            else:
                # opposite direction should use larger value (i.e. asset) to restore the position
                valueToShort = asset * (signal * -1)

            posToShort = math.floor(valueToShort / sell_price)
            if self.calcBrokerage(posToShort, sell_price) <= BROKERAGE_MIN_FEE:
                # if the volume is too small, do not execute
                return balance, longPos, shortPos, asset

            if posToShort == 0:
                pass
            elif longPos > posToShort:
                # shortPos is 0 here, reduce the longPos
                longPos -= posToShort
                balance += posToShort * sell_price - self.calcBrokerage(posToShort, sell_price)
            else:
                # extra shortPos is needed, clear all the longPos
                deltaPos = posToShort - longPos
                shortPos += deltaPos
                balance += longPos * sell_price - self.calcBrokerage(longPos, sell_price)
                longPos = 0

        asset = balance + longPos * sell_price - shortPos * buy_price
        # print("balance", balance, "longPos", longPos, "shortPos", shortPos, "asset", asset)

        # round the balance and asset value to prevent the drifting of floating values
        balance = round(balance, 2)
        asset = round(asset, 2)
        return balance, longPos, shortPos, asset

    def calculate_signals(self, ind):
        start = dt.now()
        rule_set, indicators = self._generator.create_rule_set(ind)
        data_selected = self._data[indicators]

        # Calculate the signals according to the fuzzy rule set
        decision = fuzzy.DecisionMaker(rule_set, data_selected)

        signal_data = []
        for row_index, data_row in zip(range(len(data_selected)), data_selected.iterrows()):
            dictionary = dict(data_row[1])
            signal = decision.defuzzify(dictionary)
            signal_data.append(signal)

        print("::::: [evaluator] Calculate signals ", dt.now() - start, ":::::")
        return signal_data

    def calculate_fortune(self):
        start = dt.now()
        # Calculate the fitness value according to the trading signals
        balance = 10000000  # initial amount = 10000000
        long_pos = 0
        short_pos = 0

        balance_data = []
        long_pos_data = []
        short_pos_data = []
        fortune_data = []

        for i, row in self._data.iterrows():
            balance, long_pos, short_pos, asset_value = self.execute(row, balance, long_pos,
                                                                     short_pos)
            balance_data.append(balance)
            long_pos_data.append(long_pos)
            short_pos_data.append(short_pos)
            fortune_data.append(asset_value)
            if asset_value <= 0:
                # stop the evaluation when the asset value becomes 0 or less
                print("::::: [evaluator] Calculate fitness value", dt.now() - start, ":::::")
                return None, None, None, fortune_data

        print("::::: [evaluator] Calculate fitness value", dt.now() - start, ":::::")
        return balance_data, long_pos_data, short_pos_data, fortune_data

    def evaluate(self, ind, filename=""):
        """
        Evaluate the fitness value of the Chromosome object
        The fitness value is the final wealth value after the 3-year training data

        :param ind: individual Chromosome object
        :param filename: the name of the file where the transactions to be exported to
        :return: the fitness value, i.e. wealth value
        """
        self._data['Signal'] = self.calculate_signals(ind)
        balance_data, long_pos_data, short_pos_data, fortune_data = self.calculate_fortune()

        if balance_data is None:
            #
            return fortune_data[-1]

        self._data['Fortune'] = fortune_data
        if filename:
            self._data['Balance'] = balance_data
            self._data['LongPos'] = long_pos_data
            self._data['ShortPos'] = short_pos_data
            self._data.to_csv(filename)
        return fortune_data[-1]
