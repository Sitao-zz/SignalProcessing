import fuzzy
import generator

eva_data = None


class Evaluator:

    def __init__(self, data):
        self._generator = generator.Generator(data)
        self._data = data

    @property
    def generator(self):
        return self._generator

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
        signals = decision.defuzzify(self._data)
        # TODO: need to define the data format of the signal. E.g. DataFrame with DateTimeIndex

        # Calculate the fitness value according to the trading signals

        return 0
