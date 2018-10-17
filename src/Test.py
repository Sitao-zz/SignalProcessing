
#############################################
#                                           #
#       Flow of the training process        #
#                                           #
#############################################
#import src.genetic as genetic
from src.fuzzy import DecisionMaker
from src.generator import Generator
import pandas as pd


def main():

    # Read indicators data from csv if available
    datas = pd.read_csv("AllenTest.csv")

    # instantiate DecisionMaker
    myGenerator =Generator(datas)
    print (myGenerator.items)
    myDecision = DecisionMaker( myGenerator.items,datas)

    # evaluate each record
    print('|-Stock decision Percentage-|')
    print("No ID Decision")
    for row,data in zip(range(len(datas)),datas.iterrows()):
        consequents = myDecision.defuzzify(dict(data[1]))
        print("%2i " % (row+1), end='')
        print (consequents[0][0])
        print("%.6f " % (consequents[0][1]))


    return 0

if __name__ == "__main__":
    main()

