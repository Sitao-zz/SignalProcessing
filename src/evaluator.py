import src.fuzzy as fuzzy
import src.generator as generator

eva_data = None

class Evaluator:

    def __init__(self, data):
        self._generator = generator.Generator(data)
        self._data = data

    @property
    def generator(self):
        return self._generator

    def CalcBrokerage(self,volume, price):
        BrokerageRate = 0.2
        minFee = 30
        fee = volume * price * BrokerageRate / 100
        if fee < minFee:
            return 30
        else:
            return fee

    def trade(self,data, Hold, Money):
        if data['Signal'] > 0:  # signal is buy, money must be enough to buy, otherwise can not buy
            if Money > 0:
                buy = round(Money * data['Signal'] / data['High '])
                Hold = Hold + buy
                Money = Money - buy * data['High '] - self.CalcBrokerage(buy, data['High '])
        if data['Signal'] < 0:  # signal is sell, hold must be enough to sell, otherwise can not sell
            if Hold > 0:  # data['Signal']<0
                sell = -Hold * data['Signal']
                Hold = Hold - sell
                Money = Money + sell * data['Low'] - self.CalcBrokerage(sell, data['Low'])
        fortune = Hold * data['Close'] + Money
        return Hold, Money, fortune

    def evaluate(self, ind):
        """
        Evaluate the fitness value of the Chromosome object
        The fitness value is the final wealth value after the 3-year training data

        :param ind: individual Chromosome object
        :return: the fitness value, i.e. wealth value
        """
        rule_set = self._generator.create_rule_set(ind)

        # Calculate the signals according to the fuzzy rule set
        decision = fuzzy.DecisionMaker(rule_set, self._data)

        #signals = pd.DataFrame([0.5, -0.4, 0.2, 0.4, 0.1, -0.2, -0.3, 0.2, 0.3, 0.1], index=self._data.index,columns=['Signal'])
        signals = decision.defuzzify(self._data)  #signal is a dataframe

        self._data['Signal']=signals
        # Calculate the fitness value according to the trading signals
        Hold=0
        Money=10000000
        Fortune = []
        for i, row in self._data.iterrows():
            Hold, Money, fortune = self.trade(row, Hold, Money)
            Fortune.append(fortune)
        self._data['Fortune'] = Fortune
        self._data['Operation'] = 0
        self._data.Operation[self._data.Signal > 0] = 1
        self._data.Operation[self._data.Signal < 0] = -1

        return self._data.iloc[-1,9]
