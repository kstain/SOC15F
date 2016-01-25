"""
Service Oriented Computing Lab Week12 in Python.
Service loader

Usage:
python service_loader.py

Load the service in data/service/

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    11/23/2015
"""
import yaml
import logging
from collections import OrderedDict


class Service:
    def __init__(self, name, cost, reliability, time, availability):
        """
        Model class for a single service
        :param name: Name for that service
        :param cost: Cost in
        :param reliability: reliability in %
        :param time: Time in sec
        :param availability: availability in %
        :return: Service instance
        """
        logging.basicConfig()
        self.name = name
        self.cost = cost
        self.reliability = reliability
        self.time = time
        self.availability = availability

    def to_string(self):
        return self.name + '\t' + str(self.cost) + '\t' + str(self.reliability)  \
                         + '\t' + str(self.time) + '\t' + str(self.availability)

    @property
    def ncost(self):
        """
        Normalized cost
        :return:
        """
        return self.cost / 20

    @property
    def nreliability(self):
        """
        Normalized reliability
        :return:
        """
        return self.reliability

    @property
    def ntime(self):
        """
        Normalized time
        :return:
        """
        return self.time / 2

    @property
    def navailability(self):
        """
        Normalized availability
        :return:
        """
        return self.availability


class Workflow:
    def __init__(self):
        """
        The workflow class which contains the graph of services
        :return:
        """
        self.g = []
        self.logger = logging.getLogger('workflow_logger')
        self.logger.setLevel(logging.DEBUG)

    def load(self, file):
        """
        load the dependency graph from file
        :param file: Path of the file
        :return:
        """
        with open(file, 'r') as stream:
            gfile = config=(yaml.load(stream))
        self.source = gfile['source']
        self.sink = gfile['sink']
        self.rcost = gfile['weight']['cost']
        self.rreli = gfile['weight']['reliability']
        self.rperf = gfile['weight']['performance']
        self.ravai = gfile['weight']['availability']
        self.dependencies = gfile['dependencies']
        self.services = OrderedDict()
        self.services[self.source] = 0
        self.services[self.sink] = 1
        index = 2
        for entry in self.dependencies:
            name = entry['name']
            if self.services.keys().count(name) == 0:
                self.services[name] = index

    def load_service(self, services):
        """
        Load the services dictionary
        :param services:
        :return:
        """
        self.services = services

    def get_score(self, service_dict):
        """
        Compute the score according to the given service mapping
        :param service_dict: The concrete services chosen for each service type
        :return: The score of the selection
        """
        nservice = len(service_dict)
        score_table = {}
        for k in service_dict.iterkeys():
            if k == self.source:
                cur_score = self.rcost*(-1)*service_dict[k].ncost +\
                            self.rreli*service_dict[k].nreliability +\
                            self.rperf*(-1 * service_dict[k].ntime) +\
                            self.ravai*service_dict[k].navailability
                score_table[k] = [1, service_dict[k].ncost, service_dict[k].nreliability,
                                  service_dict[k].ntime, service_dict[k].navailability, cur_score]
            else:
                score_table[k] = [-100, -100, -100, -100, -100, -100]
        for i in xrange(nservice):
            for entry in self.dependencies:
                cur_service = entry['name']
                for dep in entry['dependency']:
                    if score_table[dep][0] == -1:
                        continue
                    else:
                        cur_score = score_table[cur_service][5]
                        new_score = self.rcost*(-1 * (score_table[dep][1] + service_dict[cur_service].ncost)) +\
                                    self.rreli*(score_table[dep][2] * service_dict[cur_service].nreliability/100) +\
                                    self.rperf*(-1 * (score_table[dep][3] + service_dict[cur_service].ntime)) +\
                                    self.ravai*(score_table[dep][4] * service_dict[cur_service].navailability/100)
                        if new_score > cur_score:
                            score_table[cur_service] = [score_table[dep][0]+1,
                                                        score_table[dep][1] + service_dict[cur_service].ncost,
                                                        score_table[dep][2] * service_dict[cur_service].nreliability/100,
                                                        score_table[dep][3] + service_dict[cur_service].ntime,
                                                        score_table[dep][4] * service_dict[cur_service].navailability/100,
                                                        new_score]
                            # self.logger.debug("%s new score: %s" % (cur_service, str(new_score)))
        self.logger.info("%s new score: %s" % (self.sink, str(score_table[self.sink][5])))
        self.logger.debug("cost: %s" % str(score_table[self.sink][1]))
        self.logger.debug("reli: %s" % str(score_table[self.sink][2]))
        self.logger.debug("time: %s" % str(score_table[self.sink][3]))
        self.logger.debug("aval: %s" % str(score_table[self.sink][4]))
        return score_table[self.sink][5]

