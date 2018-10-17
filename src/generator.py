import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

DEBUGLEVEL = 0


class Generator:
    def __init__(self, data):
        self.fuzzify(data)
        self.indicatorOrder =[9,10,11,12,13]
        #self.indicators = {9: self.RSI, 10 :self.MACD , 11 : self.ADX, 12 : self.Indicator4, 13 :self.Indicator5}
        self.items = []
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

        # set up decision
        x = np.arange(0, 11, 1)
        self.decision = ctrl.Consequent(x, 'decision')
        self.decision['buy'] = fuzz.trapmf(self.decision.universe, [0, 0, 3, 4])
        self.decision['hold'] = fuzz.trapmf(self.decision.universe, [3, 4, 6, 7])
        self.decision['sell'] = fuzz.trapmf(self.decision.universe, [6, 7, 10, 10])

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
        for key in self.indicatorOrder:
            if key == 9 :
                rule1=ctrl.Rule(self.RSI['hi'], self.decision['sell'])
                rule2=ctrl.Rule(self.RSI['me'], self.decision['sell'])
                rule3 = ctrl.Rule(self.RSI['lo'], self.decision['sell'])
                rule4 = ctrl.Rule(self.RSI['hi'], self.decision['hold'])
                rule5 = ctrl.Rule(self.RSI['me'], self.decision['hold'])
                rule6 = ctrl.Rule(self.RSI['lo'], self.decision['hold'])
                rule7 = ctrl.Rule(self.RSI['hi'], self.decision['buy'])
                rule8 = ctrl.Rule(self.RSI['me'], self.decision['buy'])
                rule9 = ctrl.Rule(self.RSI['lo'], self.decision['buy'])
                self.items.append(rule1)
                self.items.append(rule2)
                self.items.append(rule3)
                self.items.append(rule4)
                self.items.append(rule5)
                self.items.append(rule6)
                self.items.append(rule7)
                self.items.append(rule8)
                self.items.append(rule9)
            elif key == 10:
                rule1 = ctrl.Rule(self.MACD['hi'], self.decision['sell'])
                rule2 = ctrl.Rule(self.MACD['me'], self.decision['sell'])
                rule3 = ctrl.Rule(self.MACD['lo'], self.decision['sell'])
                rule4 = ctrl.Rule(self.MACD['hi'], self.decision['hold'])
                rule5 = ctrl.Rule(self.MACD['me'], self.decision['hold'])
                rule6 = ctrl.Rule(self.MACD['lo'], self.decision['hold'])
                rule7 = ctrl.Rule(self.MACD['hi'], self.decision['buy'])
                rule8 = ctrl.Rule(self.MACD['me'], self.decision['buy'])
                rule9 = ctrl.Rule(self.MACD['lo'], self.decision['buy'])
                self.items.append(rule1)
                self.items.append(rule2)
                self.items.append(rule3)
                self.items.append(rule4)
                self.items.append(rule5)
                self.items.append(rule6)
                self.items.append(rule7)
                self.items.append(rule8)
                self.items.append(rule9)
            elif key == 11:
                rule1 = ctrl.Rule(self.ADX['hi'], self.decision['sell'])
                rule2 = ctrl.Rule(self.ADX['me'], self.decision['sell'])
                rule3 = ctrl.Rule(self.ADX['lo'], self.decision['sell'])
                rule4 = ctrl.Rule(self.ADX['hi'], self.decision['hold'])
                rule5 = ctrl.Rule(self.ADX['me'], self.decision['hold'])
                rule6 = ctrl.Rule(self.ADX['lo'], self.decision['hold'])
                rule7 = ctrl.Rule(self.ADX['hi'], self.decision['buy'])
                rule8 = ctrl.Rule(self.ADX['me'], self.decision['buy'])
                rule9 = ctrl.Rule(self.ADX['lo'], self.decision['buy'])
                self.items.append(rule1)
                self.items.append(rule2)
                self.items.append(rule3)
                self.items.append(rule4)
                self.items.append(rule5)
                self.items.append(rule6)
                self.items.append(rule7)
                self.items.append(rule8)
                self.items.append(rule9)
            elif key == 12:
                rule1 = ctrl.Rule(self.Indicator4['hi'], self.decision['sell'])
                rule2 = ctrl.Rule(self.Indicator4['me'], self.decision['sell'])
                rule3 = ctrl.Rule(self.Indicator4['lo'], self.decision['sell'])
                rule4 = ctrl.Rule(self.Indicator4['hi'], self.decision['hold'])
                rule5 = ctrl.Rule(self.Indicator4['me'], self.decision['hold'])
                rule6 = ctrl.Rule(self.Indicator4['lo'], self.decision['hold'])
                rule7 = ctrl.Rule(self.Indicator4['hi'], self.decision['buy'])
                rule8 = ctrl.Rule(self.Indicator4['me'], self.decision['buy'])
                rule9 = ctrl.Rule(self.Indicator4['lo'], self.decision['buy'])
                self.items.append(rule1)
                self.items.append(rule2)
                self.items.append(rule3)
                self.items.append(rule4)
                self.items.append(rule5)
                self.items.append(rule6)
                self.items.append(rule7)
                self.items.append(rule8)
                self.items.append(rule9)
            elif key == 13:
                rule1 = ctrl.Rule(self.Indicator5['hi'], self.decision['sell'])
                rule2 = ctrl.Rule(self.Indicator5['me'], self.decision['sell'])
                rule3 = ctrl.Rule(self.Indicator5['lo'], self.decision['sell'])
                rule4 = ctrl.Rule(self.Indicator5['hi'], self.decision['hold'])
                rule5 = ctrl.Rule(self.Indicator5['me'], self.decision['hold'])
                rule6 = ctrl.Rule(self.Indicator5['lo'], self.decision['hold'])
                rule7 = ctrl.Rule(self.Indicator5['hi'], self.decision['buy'])
                rule8 = ctrl.Rule(self.Indicator5['me'], self.decision['buy'])
                rule9 = ctrl.Rule(self.Indicator5['lo'], self.decision['buy'])
                self.items.append(rule1)
                self.items.append(rule2)
                self.items.append(rule3)
                self.items.append(rule4)
                self.items.append(rule5)
                self.items.append(rule6)
                self.items.append(rule7)
                self.items.append(rule8)
                self.items.append(rule9)
            else:
                print('Invlid indicator index :'+str( key))


    def create_rule_set(self, ind):
        """
        Create the rule set according to the individual indexes

        :param ind: the individual containing the indexes for the selected rule
        :return: the list of control rules
        """
        print (self.items)
        return self.items
