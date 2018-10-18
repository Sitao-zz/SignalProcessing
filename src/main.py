
#############################################
#                                           #
#       Flow of the training process        #
#                                           #
#############################################
from src.genetic import GeneticEngine
import pandas as pd


# Get the best individual and its fitness value
data = pd.read_csv("data\TrainDataWithInds.csv")
engine = GeneticEngine(data)
best_ind = engine.best_ind()

evaluator = engine.evaluator
value = evaluator.evaluate(best_ind)
