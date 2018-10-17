import src.evaluator as eva
import random
import numpy

from deap import tools, creator, base, algorithms

IND_INIT_SIZE = 30 # 基因编码位数 (10 rules * 3)
MAX_ITEM = 50
MAX_WEIGHT = 50
NBR_ITEMS = 100

# To assure reproductibility, the RNG seed is set prior to the items
# dict initialization. It is also seeded in main().
random.seed(64)

# Create the item dictionary: item name is an integer, and value is
# a (weight, value) 2-uple.
items = {}
# Create random items and store them in the items' dictionary.
for i in range(NBR_ITEMS):
    items[i] = (random.randint(1, 10), random.uniform(0, 100))

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", set, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
#       define 'attr_item' to be an attribute ('gene')
#       which corresponds to integers sampled uniformly
#       from the range [1,10] (i.e. 1 to 10 with equal probability)
toolbox.register("attr_item", random.random, NBR_ITEMS)

# Structure initializers
#       define 'individual' to be an individual
#       consisting of 100 'attr_bool' elements ('genes')
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_item, IND_INIT_SIZE)

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

class GeneticEngin:

    def __init__(self, data):
        self._evaluator = eva.Evaluator(data)

    @property
    def evaluator(self):
        return self._evaluator

    def eval_ind(self, ind):
        """
        calculate the fitness of the individual

        :param ind: the individual Chromosome object to be evaluated
        :return: the fitness value
        """
        return self._evaluator.evaluate(ind)

    def mutate_ind(self, ind, mu=0, sigma=4, chance_mutation=0.4):
        """
        Mutate the individual by changing the Chromosome composition
        :param mu:
        :param sigma:
        :return:
        """
        if random.random() < chance_mutation:
            if len(ind) > 0:  # We cannot pop from an empty set
                ind.remove(random.choice(sorted(tuple(ind))))
        else:
            ind.add(random.randrange(NBR_ITEMS))
        return ind

    def cx_ind(self, ind1, ind2, chance_crossover=0.7):
        """Apply a crossover operation on input sets. The first child is the
        intersection of the two sets, the second child is the difference of the
        two sets.
        """
        if random.random() < chance_crossover:
            temp = set(ind1)  # Used in order to keep type
            ind1 &= ind2  # Intersection (inplace)
            ind2 ^= temp  # Symmetric Difference (inplace)
        return ind1, ind2

    toolbox.register("evaluate", eval_ind)
    toolbox.register("mate", cx_ind)
    toolbox.register("mutate", mutate_ind)
    toolbox.register("select", tools.selNSGA2)

    def verify_ind(self, ind):
        """
        Verify the validity of the individual Chromosome

        :param ind: the individual Chromosome to be verified
        :return: True if the Chromosome is valid, False otherwise
        """
        # TODO: will it be better if we define the method as the member method of Chromosome?
        return True

    def best_ind(self):
        """
        Get the best individual after the GA calculation

        :return: the best individual Chromosome
        """
        random.seed(64)
        NGEN = 50
        MU = 50
        LAMBDA = 100
        CXPB = 0.7
        MUTPB = 0.2

        pop = toolbox.population(n=MU)
        hof = tools.ParetoFront()
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean, axis=0)
        stats.register("std", numpy.std, axis=0)
        stats.register("min", numpy.min, axis=0)
        stats.register("max", numpy.max, axis=0)
        algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats,
                                  halloffame=hof)
        return hof[-1]
