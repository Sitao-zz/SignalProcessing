import src.evaluator as eva

from deap import tools


class GeneticEngine:
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

        :param ind: the individual Chromosome object to be mutated
        :param mu:
        :param sigma:
        :param chance_mutation:
        :return:
        """
        return ind

    def cx_ind(self, ind1, ind2):
        """
        Cross-over the two individual Chromosome objects by changing its gene (i.e. RuleDescriptor object)

        :param ind1: the 1st Chromosome object
        :param ind2: the 2nd Chromosome object
        :return: the two new individual Chromosome objects
        """

        return ind1, ind2

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
        hof = tools.ParetoFront()
        return hof[-1]
