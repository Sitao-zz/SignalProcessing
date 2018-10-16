import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

DEBUGLEVEL = 0


class Generator:
    def __init__(self, data):
        self.ADX = None
        self.RSI = None
        self.MACD = None
        self.Indicator4=None
        self.Indicator5 = None
        self.decision = None
        self.indicatorOrder =[9,10,11,12,13]
        self.indicators = {9: self.RSI, 10 :self.MACD , 11 : self.ADX, 12 : self.Indicator4, 13 :self.Indicator5}
        self.items = {}
        self.fuzzify(data)
        self.init_rules(data)

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
        self.RSI = ctrl.Antecedent(x, data.columns[9])
        self.RSI['lo'] = fuzz.trimf(x, [0, 0, 30])
        self.RSI['me'] = fuzz.trimf(x, [20, 50, 90])
        self.RSI['hi'] = fuzz.trimf(x, [80, 100, 100])

        # set up MACD
        x = np.arange(0, 101, 1)
        self.MACD = ctrl.Antecedent(x, data.columns[10])
        self.MACD['lo'] = fuzz.trimf(x, [0, 0, 30])
        self.MACD['me'] = fuzz.trimf(x, [20, 50, 90])
        self.MACD['hi'] = fuzz.trimf(x, [80, 100, 100])

        # set up other Indicators membership functions
        # ADX
        x = np.arange(0, 101, 1)
        self.ADX = ctrl.Antecedent(x, data.columns[11])
        self.ADX['lo'] = fuzz.trimf(x, [0, 0, 30])
        self.ADX['me'] = fuzz.trimf(x, [20, 50, 90])
        self.ADX['hi'] = fuzz.trimf(x, [80, 100, 100])

        x = np.arange(0, 101, 1)
        self.Indicator4 = ctrl.Antecedent(x, data.columns[12])
        self.Indicator4['lo'] = fuzz.trimf(x, [0, 0, 30])
        self.Indicator4['me'] = fuzz.trimf(x, [20, 50, 90])
        self.Indicator4['hi'] = fuzz.trimf(x, [80, 100, 100])

        x = np.arange(0, 101, 1)
        self.Indicator5 = ctrl.Antecedent(x, data.columns[13])
        self.Indicator5['lo'] = fuzz.trimf(x, [0, 0, 30])
        self.Indicator5['me'] = fuzz.trimf(x, [20, 50, 90])
        self.Indicator5['hi'] = fuzz.trimf(x, [80, 100, 100])

        return

    def init_rules(self,data):
        """
        This method:
        (1) sets the rule base
        (2) sets the inference engine to use the rule base
        :return: void
        """
        # TODO: dynamically generating the rules and add them into the item dictionary
        # store the rules into the dictionary

        counter = 0
        for key, value in self.indicators.items():
            if key in self.indicatorOrder:
                self.items[counter].append(ctrl.Rule(value['hi'], self.decision['sell']))
                self.items[counter + 1].append(ctrl.Rule(value['me'], self.decision['sell']))
                self.items[counter + 2].append(ctrl.Rule(value['lo'], self.decision['sell']))
                self.items[counter + 3].append(ctrl.Rule(value['hi'], self.decision['hold']))
                self.items[counter + 4].append(ctrl.Rule(value['me'], self.decision['hold']))
                self.items[counter + 5].append(ctrl.Rule(value['lo'], self.decision['hold']))
                self.items[counter + 6].append(ctrl.Rule(value['hi'], self.decision['buy']))
                self.items[counter + 7].append(ctrl.Rule(value['me'], self.decision['buy']))
                self.items[counter + 8].append(ctrl.Rule(value['lo'], self.decision['buy']))
                counter = counter + 9
            else:
                print(key,value)


    def create_rule_set(self, ind):
        """
        Create the rule set according to the individual indexes

        :param ind: the individual containing the indexes for the selected rule
        :return: the list of control rules
        """
        return self.items
