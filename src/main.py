#############################################
#                                           #
#       Flow of the training process        #
#                                           #
#############################################
from src.genetic import GeneticEngine
from src.dataProcessing_Daily import DataProcessing_Daily
from src.dataProcessing import DataProcessing
import pandas as pd
from datetime import datetime as dt

preprocess = False

# Get the best individual and its fitness value
start = dt.now()
if preprocess:
    df = pd.read_excel("data/FCPO_2011_2013.xlsx", "2011-2013")
    dataprocessing_Daily = DataProcessing_Daily(df)
    data = dataprocessing_Daily.Preprocessing_Daily(df)

    # dataprocessing= DataProcessing(df)
    # data=dataprocessing.Preprocessing(df)
    pass
else:
    data = pd.read_csv('data\TrainDataWithInds_Daily.csv')
print("::::: [main] Load data", dt.now() - start, ":::::")

start = dt.now()
engine = GeneticEngine(data)
print("::::: [main] Initialize GeneticEngine", dt.now() - start, ":::::")

start = dt.now()
best_ind = engine.best_ind()
if best_ind is None:
    print("::::: [main] Find the best individual", dt.now() - start, ":::::")
    evaluator = engine.evaluator
    value = evaluator.evaluate(best_ind, "data/transactions_best.csv")
    print("\n:::: [genetic] best individual", best_ind, "fitness value", value, "::::")
else:
    print("::::: [main] No individual found with positive fitness value", dt.now() - start, ":::::")
