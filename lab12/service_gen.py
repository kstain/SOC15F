"""
Service Oriented Computing Lab Week12 in Python.
Service Generator

Usage:
python service_gen.py

Generate services according to the name and number listed in service/service_list.yaml
The output will be in data/service/

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    11/23/2015
"""
from service import Service
import random
import yaml


def service_generator(name):
    sn = 1
    while True:
        s = Service(name+'_'+str(sn), random.randint(0, 200), random.randint(0, 100), random.randint(0, 20),
                    random.randint(0, 100))
        yield s
        sn += 1

if __name__ == '__main__':
    config = {}
    with open('data/service_list.yaml', 'r') as stream:
        config=(yaml.load(stream))
    service_list = config['services']
    for item in service_list:
        sg = service_generator(item['name'])
        with open('data/service/%s'%item['name'], 'w') as ofstream:
            for i in xrange(item['count']):
                ofstream.write(next(sg).to_string()+'\n')
