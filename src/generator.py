import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

DEBUGLEVEL = 0


class Generator:
    def __init__(self, data):
        self.ADX = None
        self.RSI = None
        self.MACD = None
        self.decision = None
        self.items = {}
        self.fuzzify(data)
        self.init_rules()


    def fuzzify(self, data):
        """
        This method performs the fuzzification:
        (1) sets the fuzzy partitions of each linguistic variable and
        (2) sets the membership function of each linguistic term of the variable

        :param data:
        :return:
        """

        # set up RSI
        x = np.arange(0, 101, 1)
        self.RSI = ctrl.Antecedent(x, data.columns[1])

        self.RSI['lo'] = fuzz.trimf(x, [0, 0, 30])
        self.RSI['me'] = fuzz.trimf(x, [20, 50, 90])
        self.RSI['hi'] = fuzz.trimf(x, [80, 100, 100])

        # set up MACD
        x = np.arange(0, 201, 1)
        self.MACD = ctrl.Antecedent(x, data.columns[2])
        self.MACD['lo'] = fuzz.trapmf(self.MACD.universe, [0, 0, 20, 30])
        self.MACD['me'] = fuzz.trapmf(self.MACD.universe, [30, 50, 80, 100])
        self.MACD['hi'] = fuzz.trapmf(self.MACD.universe, [80, 100, 200, 200])

        # self.MACD['lo'] = fuzz.trimf(x, [0, 0, 30])
        # self.MACD['me'] = fuzz.trimf(x, [20, 50, 90])
        # self.MACD['hi'] = fuzz.trimf(x, [80, 100, 100])

        # set up ADX
        x = np.arange(20, 101, 1)
        self.ADX = ctrl.Antecedent(x, data.columns[3])
        self.ADX['lo'] = fuzz.trapmf(self.ADX.universe, [20, 20, 30, 40])
        self.ADX['me'] = fuzz.trapmf(self.ADX.universe, [30, 40, 50, 60])
        self.ADX['hi'] = fuzz.trapmf(self.ADX.universe, [50, 60, 100, 100])

        # set up decision
        x = np.arange(0, 11, 1)
        self.decision = ctrl.Consequent(x, 'decision')
        self.decision['buy'] = fuzz.trapmf(self.decision.universe, [0, 0, 3, 4])
        self.decision['hold'] = fuzz.trapmf(self.decision.universe, [3, 4, 6, 7])
        self.decision['sell'] = fuzz.trapmf(self.decision.universe, [6, 7, 10, 10])

        if DEBUGLEVEL == 1:
            self.RSI.view()
            self.MACD.view()
            self.ADX.view()
            self.decision.view()
        return

    def init_rules(self):
        """
        This method:
        (1) sets the rule base
        (2) sets the inference engine to use the rule base
        :return: void
        """

        # TODO: dynamically generating the rules and add them into the item dictionary

        # rules 01 - 27
        # RSI & MACD & ADX -> decision (buy, hold, sell)
        rule01 = ctrl.Rule(self.MACD['hi'], self.decision['sell'])
        rule02 = ctrl.Rule(self.MACD['me'], self.decision['sell'])
        rule03 = ctrl.Rule(self.MACD['lo'], self.decision['sell'])
        rule04 = ctrl.Rule(self.MACD['hi'], self.decision['hold'])
        rule05 = ctrl.Rule(self.MACD['me'], self.decision['hold'])
        rule06 = ctrl.Rule(self.MACD['lo'], self.decision['hold'])
        rule07 = ctrl.Rule(self.MACD['hi'], self.decision['buy'])
        rule08 = ctrl.Rule(self.MACD['me'], self.decision['buy'])
        rule09 = ctrl.Rule(self.MACD['lo'], self.decision['buy'])

        # store the rules into the dictionary
        self.items[0] = rule01

        return

    def create_rule_set(self, ind):
        """
        Create the rule set according to the individual indexes

        :param ind: the individual containing the indexes for the selected rule
        :return: the list of control rules
        """
        return [self.items[0], self.items[1]]
