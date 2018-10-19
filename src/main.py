
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
data = pd.read_csv("data\TrainDataWithInds.csv")
print(":::::Load data ", dt.now() - start, ":::::")

start = dt.now()
engine = GeneticEngine(data)
print(":::::Initialize GeneticEngine ", dt.now() - start, ":::::")

start = dt.now()
best_ind = engine.best_ind()
print(":::::Find the best individual ", dt.now() - start, ":::::")

evaluator = engine.evaluator
value = evaluator.evaluate(best_ind)
