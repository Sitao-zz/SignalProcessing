from skfuzzy import control as ctrl


class DecisionMaker:

    def __init__(self, rule_set, data):
        """
        Constructor, set up control system for decision
        :param rule_set: the rule_set used to create the
        """
        self.column_names = data.columns
        self.decisionCS = ctrl.ControlSystem(rule_set)
        self.decisionEval = ctrl.ControlSystemSimulation(self.decisionCS)

    def defuzzify(self, data_row):
        """
        This function evaluates the given data with inference engine
        and defuzzifies the output
        Returns decision

        :param data_row:
        :return: signal showing the operation degree in [-1, 1]
        """

        for name in self.column_names:
            self.decisionEval.input[name] = data_row[name]

        signal = 0.0
        try:
            self.decisionEval.compute()
            signal = round((self.decisionEval.output['decision'] - 5) / 10, 2)
        except ValueError as err:
            # print(err)
            pass

        # consequences[0][0]  is DateTime Index  20110103-10:38:00
        # consequences[0][1]  is decision  e.g. 0.2  , -0.3

        # return decision
        return signal
