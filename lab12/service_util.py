"""
Service Oriented Computing Lab Week12 in Python.
Service Generator and loader

generator:
Usage:
python service_util.py

Generate services according to the name and number listed in service/service_list.yaml
The output will be in data/service/

Loader:
Load the service in data/service/

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    11/23/2015
"""
import random
import yaml
import os
from os import path
import collections

from service import Service


def service_generator(name):
    sn = 1
    while True:
        s = Service(name+'_'+str(sn), random.randint(1, 200), random.randint(1, 100), random.randint(1, 20),
                    random.randint(1, 100))
        yield s
        sn += 1


class ServiceLoader:
    def __init__(self, file_path='data/service'):
        self.files = [path.join(file_path, f) for f in os.listdir(file_path) if path.isfile(path.join(file_path, f))]
        self.services = collections.OrderedDict()
        for file in self.files:
            self.services[path.basename(file)] = []
            with open(file, 'r') as stream:
                for line in stream.read().splitlines():
                    [name, cost, reliability, time, availability] = line.split('\t')
                    svc = Service(name, float(cost), float(reliability), float(time), float(availability))
                    self.services[path.basename(file)].append(svc)


if __name__ == '__main__':
    config = {}
    with open('data/service_list.yaml', 'r') as stream:
        config = (yaml.load(stream))
    service_list = config['services']
    for item in service_list:
        sg = service_generator(item['name'])
        with open('data/service/%s'%item['name'], 'w') as ofstream:
            for i in xrange(item['count']):
                ofstream.write(next(sg).to_string()+'\n')
