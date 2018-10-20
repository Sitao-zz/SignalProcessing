#############################################
#                                           #
#       Flow of the training process        #
#                                           #
#############################################
from src.genetic import GeneticEngine
import pandas as pd
from datetime import datetime as dt

# Get the best individual and its fitness value
start = dt.now()
data = pd.read_csv("data\TrainDataWithInds_trim.csv")
print("::::: [main] Load data ", dt.now() - start, ":::::")

start = dt.now()
engine = GeneticEngine(data)
print("::::: [main] Initialize GeneticEngine ", dt.now() - start, ":::::")

start = dt.now()
best_ind = engine.best_ind()
print("::::: [main] Find the best individual ", dt.now() - start, ":::::")

evaluator = engine.evaluator
value = evaluator.evaluate(best_ind)
