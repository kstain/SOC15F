"""
Service Oriented Computing Lab Week12 in Python.
Service selector for workflow using generic algorithm

Usage:
python ga.py -w PATH_TO_WORKFLOW [-s PATH_TO_SERVICE_DIR]

-w is tha path to the workflow yaml file
-s is the path to the dir of services

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    11/23/2015
"""
import array
import random

from argparse import ArgumentParser

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from service_util import ServiceLoader
from service import *


class ServiceSelector:
    def __init__(self, wf_path, svc_path=''):
        """
        Service Selector class using GA
        :param wf_path: The workflow file path
        :param svc_path: Dir path for the services
        :return:
        """
        self.wf = Workflow()
        self.wf.load(wf_path)
        if svc_path == '':
            loader = ServiceLoader()
        else:
            loader = ServiceLoader(svc_path)
        self.svc = loader.services

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()

        # Attribute generator
        self.toolbox.register("attr_num", random.randint, 0, 100)

        # Structure initializers
        self.toolbox.register("individual", tools.initRepeat, creator.Individual,
                              self.toolbox.attr_num, len(self.wf.services))
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        def evalFitness(individual):
            """
            Evaluate the fitness using the WorkFlow class
            :param individual: The selected concrete services
            :return: The fitness score
            """
            service_dict = OrderedDict()
            for k, v in self.wf.services.iteritems():
                count = len(self.svc[k])
                service_dict[k] = self.svc[k][individual[v] % count]
            return self.wf.get_score(service_dict),

        self.toolbox.register("evaluate", evalFitness)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutUniformInt, low=0, up=100, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def getResult(self, pop):
        """
        Interpret the population integers to the selection result
        :param pop: population
        :return:
        """
        service_dict = OrderedDict()
        for k, v in self.wf.services.iteritems():
            count = len(self.svc[k])
            service_dict[k] = self.svc[k][pop[0][v] % count].name
        return service_dict

    def run(self):
        """
        Run GA to get the highest fitness population
        :return: The population after iterations
        """
        random.seed(64)
        pop = self.toolbox.population(n=30)
        hof = tools.HallOfFame(1)
        pop, log = algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=100,
                                       halloffame=hof, verbose=True)
        print self.getResult(pop)
        return pop

if __name__ == "__main__":
    parser = ArgumentParser(description='Server arguments.')
    parser.add_argument('-w', metavar='workflow', help='input workflow.')
    parser.add_argument('-s', metavar='service', default='data/service', help='input service.')
    po = parser.parse_args()
    ga_sel = ServiceSelector(po.w, po.s)
    ga_sel.run()

