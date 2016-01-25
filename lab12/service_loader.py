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
import os
from os import path
import collections
from service import Service


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
