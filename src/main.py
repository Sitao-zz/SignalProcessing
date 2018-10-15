
#############################################
#                                           #
#       Flow of the training process        #
#                                           #
#############################################
import genetic


# Get the best individual and its fitness value
data = None  # TODO: need to get the training data
engine = genetic.GeneticEngin(data)
best_ind = engine.best_ind()

evaluator = engine.evaluator
value = evaluator.evaluate(best_ind)
