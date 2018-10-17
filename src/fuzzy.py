from skfuzzy import control as ctrl

###############################################################################
# constants

NUM_VARIABLES = 3  # 4 variables


###############################################################################

class DecisionMaker:

    def __init__(self, rule_set, data):
        """
        Constructor, set up control system for decision
        :param rule_set: the rule_set used to create the
        """
        self.dataheaders = data.columns
        self.decisionCS = ctrl.ControlSystem(rule_set)
        self.decisionEval = ctrl.ControlSystemSimulation(self.decisionCS)

    def defuzzify(self, data):
        """
        This function evaluates the given data with inference engine
        and defuzzifies the output
        Returns decision

        :param data:
        :return:
                                            degree
        date
        2014-05-01 18:47:05.069722            NaN
        2014-05-01 18:47:05.119994            0.2
        2014-05-02 18:47:05.178768            0.1
        2014-05-02 18:47:05.230071           -0.3
        2014-05-02 18:47:05.230071            0.4
        2014-05-02 18:47:05.280592           -0.2
        2014-05-03 18:47:05.332662            0.4
        2014-05-03 18:47:05.385109           -0.6
        2014-05-04 18:47:05.436523           -0.8
        2014-05-04 18:47:05.486877            0.9
        """

        self.decisionEval.input[self.dataheaders[9]] = data[self.dataheaders[9]]
        self.decisionEval.input[self.dataheaders[10]] = data[self.dataheaders[10]]
        self.decisionEval.input[self.dataheaders[11]] = data[self.dataheaders[11]]
        self.decisionEval.input[self.dataheaders[12]] = data[self.dataheaders[12]]
        self.decisionEval.input[self.dataheaders[13]] = data[self.dataheaders[13]]
        self.decisionEval.compute()
        decision = round((self.decisionEval.output['decision'] - 5) / 10,2)

        consequents = [[]]
        consequents[0] = [data[self.dataheaders[3]], decision]

        # consequents[0][0]  is DateTime Index  20110103-10:38:00
        # consequents[0][1]  is decision  e.g. 0.2  , -0.3

        # return decision
        return consequents
