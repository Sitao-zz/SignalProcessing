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

        if not self.checkData(data):
            return

        self.decisionCS = ctrl.ControlSystem(rule_set)
        self.decisionEval = ctrl.ControlSystemSimulation(self.decisionCS)

    def checkData(self, data):
        """
        This method verifies the correctness of the data:
        (1) checks correct number of variables
        (2) checks at least one row of data exists

        :param data:
        :return:
        """
        if len(data.columns) < NUM_VARIABLES:
            print("Insufficient fuzzy variables")
            return False

        if len(data) == 0:
            print("No data found")
            return False

        self.dataheaders = data.columns
        return True

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

        self.decisionEval.input[self.dataheaders[1]] = data[self.dataheaders[1]]
        self.decisionEval.input[self.dataheaders[2]] = data[self.dataheaders[2]]
        self.decisionEval.input[self.dataheaders[3]] = data[self.dataheaders[3]]
        self.decisionEval.compute()
        decision = (self.decisionEval.output['decision'] - 5) / 10

        consequences = [[]]
        consequences[0] = [decision]

        # return decision
        return consequences
