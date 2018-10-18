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
    #print(myGenerator.rules)

    # {0-8: self.RSI, 9-17 :self.MACD , 18-26 : self.ADX, 26-35 : self.Indicator4, 35-44 :self.Indicator5}
    individual = [0, 1, 4, 7, 9, 16, 19]
    rules, indicators = myGenerator.create_rule_set(individual)
    data_selected = data_indicator[indicators]
    myDecision = DecisionMaker(rules, data_selected)

    myEvaluator=Evaluator(data)
    myEvaluator.evaluate(individual)

    print (rules)



    # evaluate each record

    print('|-Stock decision Percentage-|')
    print("No Decision")
    for row, data_selected in zip(range(len(data_selected)), data_selected.iterrows()):
        consequents = myDecision.defuzzify(dict(data_selected[1]))
        print("%2i " % (row + 1), end='')
        print("%.6f " % (consequents[0][0]))

    return 0


if __name__ == "__main__":
    main()
