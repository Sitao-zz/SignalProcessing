import src.fuzzy as fuzzy
from src.generator import Generator
from datetime import datetime as dt


class Evaluator:

    def __init__(self, data):
        data_indicator = data.iloc[:, range(9, len(data.columns), 1)]
        self._generator = Generator(data_indicator)
        self._data = data

    @property
    def generator(self):
        return self._generator

    def calcBrokerage(self, volume, price):
        brokerageRate = 0.2
        minFee = 30
        fee = volume * price * brokerageRate / 100
        if volume == 0 | price == 0:
            return 0
        elif fee < minFee:
            return 30
        else:
            return fee

    # Execute trade and return Long position, Short Position.
    # Update and return new Short Price if there is short instrument executed.
    def execute(self, data, balance, longPos, shortPos, lastShortPrice):

        unrealizedShortValue = shortPos * (lastShortPrice - data['High '])
        unrealizedLongValue = longPos * data['High ']

        if data['Signal'] > 0:

            valueToLong = (balance + unrealizedShortValue) * data['Signal']

            if valueToLong > unrealizedShortValue:
                posToBuy = round(valueToLong / data['Low'])
                longPos = longPos + posToBuy
                balance = balance + unrealizedShortValue - valueToLong - self.calcBrokerage(shortPos, data[
                    'High ']) - self.calcBrokerage(posToBuy, data['Low'])
                shortPos = 0
                lastShortPrice = 0
            else:
                posToLong = round(valueToLong / data['High '])
                shortPos = shortPos - posToLong
                balance = balance + shortPos * (lastShortPrice - data['High ']) - self.calcBrokerage(posToLong,
                                                                                                    data['High '])
                longPos = 0
                lastShortPrice = data['Low']

        elif data['Signal'] < 0:

            valueToShort = (balance + unrealizedLongValue) * data['Signal']

            if valueToShort > unrealizedLongValue:
                posToShort = round(valueToShort / data['High '])
                shortPos = shortPos + posToShort
                balance = balance + longPos * data['High '] - self.calcBrokerage(longPos,
                                                                                data['Low']) - self.calcBrokerage(
                    posToShort, data['Low'])
                longPos = 0
                lastShortPrice = data['Low']
            else:
                posToShort = round(valueToShort / data['Low'])
                longPos = longPos - posToShort
                balance = balance - valueToShort - self.calcBrokerage(posToShort, data['High '])
                shortPos = 0
                lastShortPrice = 0

        assetValue = balance + longPos * data['Low'] + shortPos * (lastShortPrice - data['High '])
        return balance, longPos, shortPos, lastShortPrice, assetValue

    def evaluate(self, ind):
        """
        Evaluate the fitness value of the Chromosome object
        The fitness value is the final wealth value after the 3-year training data

        :param ind: individual Chromosome object
        :return: the fitness value, i.e. wealth value
        """
        start = dt.now()
        # rule_set = self._generator.create_rule_set(ind)
        rule_set, indicators = self._generator.create_rule_set(ind)
        data_selected = self._data[indicators]

        # Calculate the signals according to the fuzzy rule set
        decision = fuzzy.DecisionMaker(rule_set, data_selected)

        # signals = pd.DataFrame([0.5, -0.4, 0.2, 0.4, 0.1, -0.2, -0.3, 0.2, 0.3, 0.1]
        # index=self._data.index,columns=['Signal'])

        signals = []
        # signals = decision.defuzzify(self._data)  #signal is a dataframe
        for row_index, data_row in zip(range(len(data_selected)), data_selected.iterrows()):
            dictionary = dict(data_row[1])
            signal = decision.defuzzify(dictionary)
            signals.append(signal)

        self._data['Signal'] = signals
        print("::::: [evaluator] Calculate signals ", dt.now() - start, ":::::")

        start = dt.now()
        # Calculate the fitness value according to the trading signals
        Balance = 10000000  # initial amount = 10000000
        AssetValue = 0
        LongPosition = 0
        ShortPosition = 0
        LastShortPrice = 0
        Fortune = []

        for i, row in self._data.iterrows():
            Balance, LongPosition, ShortPosition, LastShortPrice, AssetValue = self.execute(row, Balance, LongPosition,
                                                                                            ShortPosition,
                                                                                            LastShortPrice)
            Fortune.append(AssetValue)
        self._data['Fortune'] = Fortune
        # self._data['Operation'] = 0
        # self._data.Operation[self._data.Signal > 0] = 1
        # self._data.Operation[self._data.Signal < 0] = -1
        fit_val = self._data.iloc[-1]['Fortune']

        print("::::: [evaluator] Calculate fitness value", dt.now() - start, ":::::")
        return fit_val
