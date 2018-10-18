#############################################
#                                           #
#       Flow of the training process        #
#                                           #
#############################################
# import src.genetic as genetic
import unittest
import pandas as pd
from src.evaluator import Evaluator


class TestEvaluatorMethods(unittest.TestCase):
    def test_evaluate_ind(self):
        # Read indicators data from csv if available
        data = pd.read_csv("test_data_fuzzy.csv")

        # instantiate DecisionMaker
        myEvaluator = Evaluator(data)
        myGenerator = myEvaluator.generator
        print(myGenerator.rules)

        # {0-8: self.RSI, 9-17 :self.MACD , 18-26 : self.ADX, 26-35 : self.Indicator4, 35-44 :self.Indicator5}
        individual = [0, 3, 5, 9, 13, 15, 18, 21, 25, 28, 30, 35, 40, 42, 43]

        # evaluate each record
        fit_val = myEvaluator.evaluate(individual)
        print(fit_val)
        self.assertTrue(fit_val is not None)


if __name__ == "__main__":
    unittest.main()
