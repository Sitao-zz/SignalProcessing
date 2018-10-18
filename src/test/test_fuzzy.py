#############################################
#                                           #
#       Flow of the training process        #
#                                           #
#############################################
# import src.genetic as genetic
from src.fuzzy import DecisionMaker
from src.generator import Generator
import pandas as pd
from src.evaluator import  Evaluator


def main():
    # Read indicators data from csv if available
    data = pd.read_csv("test_data_fuzzy.csv")
    data_indicator = data.iloc[:,range(9,len(data.columns),1)]
    #print(data_indicator)

    # instantiate DecisionMaker
    myGenerator = Generator(data_indicator)
    print(myGenerator.rules)

    # {0-8: self.RSI, 9-17 :self.MACD , 18-26 : self.ADX, 26-35 : self.Indicator4, 35-44 :self.Indicator5}
    individual = [0,3,5, 9,13,15, 18,21,25, 28,30,35, 40,42,43]
    rules, indicators = myGenerator.create_rule_set(individual)
    data_selected = data_indicator[indicators]
    myEvaluator=Evaluator(myGenerator,data)
    myEvaluator.evaluate(individual)
    print (rules)

    # evaluate each record




if __name__ == "__main__":
    main()
