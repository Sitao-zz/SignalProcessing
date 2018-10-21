import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

DEBUGLEVEL = 0


class Generator:
    def __init__(self, data):
        self.indicators = data.columns
        self.ind_funcs = []
        self.decision = None
        self.rules = []
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

        # Setup 0 based index representing the indicator
        # indicator col_index
        # RSI       0
        # MACD      1
        # ADX       2

        for name in self.indicators:
            # set up indicator after the cffset columns
            max = data[name].max()
            min = data[name].min()
            mean = data[name].mean()
            llb = round(min - (max - min) * 0.1, 2)
            lrb = round(min + (mean - min) * 0.6, 2)
            mlb = round(min + (mean - min) * 0.4, 2)
            mid = round(mean, 2)
            mrb = round(mean + (max - mean) * 0.8, 2)
            hlb = round(mean + (max - mean) * 0.6, 2)
            hrb = round(max + (max - min) * 0.1, 2)

            x = np.arange(llb, hrb, 0.01)
            # column starts from the one after the offset
            indicator = ctrl.Antecedent(x, name)
            indicator['lo'] = fuzz.trimf(x, [llb, llb, lrb])
            indicator['me'] = fuzz.trimf(x, [mlb, mid, mrb])
            indicator['hi'] = fuzz.trimf(x, [hlb, hrb, hrb])
            self.ind_funcs.append(indicator)

            # if name == "SMA10":
            #     indicator.view()
            #     print("low left boundary value : " + str(llb) + " low right boundary value : " + str(lrb))
            #     print("medium left boundary value : " + str(mlb))
            #     print("middle value : " + str(mid))
            #     print("medium right boundary value :" + str(mrb))
            #     print("high left boundary value : " + str(hlb))
            #     print("high right boundary value : " + str(hrb))

        # set up decision
        x = np.arange(0, 11, 1)
        self.decision = ctrl.Consequent(x, 'decision')
        self.decision['buy'] = fuzz.trapmf(self.decision.universe, [0, 0, 3, 4])
        self.decision['hold'] = fuzz.trapmf(self.decision.universe, [3, 4, 6, 7])
        self.decision['sell'] = fuzz.trapmf(self.decision.universe, [6, 7, 10, 10])
        return

    def init_rules(self):
        """
        This method:
        (1) sets the rule base
        (2) sets the inference engine to use the rule base
        :return: void
        """
        # TODO: dynamically generating the rules and add them into the item dictionary
        # store the rules into the dictionary

        for indicator in self.ind_funcs:
            self.rules.append(ctrl.Rule(indicator['hi'], self.decision['sell']))
            self.rules.append(ctrl.Rule(indicator['me'], self.decision['sell']))
            self.rules.append(ctrl.Rule(indicator['lo'], self.decision['sell']))
            self.rules.append(ctrl.Rule(indicator['hi'], self.decision['hold']))
            self.rules.append(ctrl.Rule(indicator['me'], self.decision['hold']))
            self.rules.append(ctrl.Rule(indicator['lo'], self.decision['hold']))
            self.rules.append(ctrl.Rule(indicator['hi'], self.decision['buy']))
            self.rules.append(ctrl.Rule(indicator['me'], self.decision['buy']))
            self.rules.append(ctrl.Rule(indicator['lo'], self.decision['buy']))
        print('Rule set size:%d' % (len(self.rules)))
        return

    def create_rule_set(self, ind):
        """
        Create the rule set according to the individual indexes

        :param ind: the individual containing the indexes for the selected rule
        :return: the list of control rules
        """
        rules = []
        indicators = []
        for i in ind:
            assert (i < len(self.rules))
            assert (i // 9 < len(self.indicators))

            rules.append(self.rules[i])
            indicator = self.indicators[i // 9]
            if indicator not in indicators:
                indicators.append(indicator)

        return rules, indicators
