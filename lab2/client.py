#!/usr/bin/env python
"""
Service Oriented Computing Week2 Lab
Client example

Using suds to consume wsdl and call the service.

Usage: 
python client.py [-a IP] [-p PORT] -f FILE
or use -h to view help message

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    9/13/2015
"""

from suds.client import Client
from argparse import ArgumentParser
import yaml

parser = ArgumentParser(description='Calculator arguments.')
parser.add_argument('-a', metavar='IP', default='', 
                    help='ip listened.')
parser.add_argument('-p', metavar='PORT', type=int,
                    help='port listened')
parser.add_argument('-f', metavar='FILE', type=str,
                    help='request YAML file')
po = parser.parse_args()

  
address = 'localhost' if len(po.a)==0 else po.a
address = ':'.join([address, str(po.p)])

query_client = Client('http://%s/?wsdl' % address)

requests = {}
with open(po.f, 'r') as stream:
  requests=(yaml.load(stream))
  

for request in requests['requests']:
  type = request['type']
  if (type=='query_coauthor'):
    print("\n=======query_coauthor on %s , result is========\n"%request['name'])
    print(query_client.service.query_coauthor(request['name']))
  elif (type=='query_by_name'):
    print("\n=======query_by_name on %s , result is========\n"%request['title'])
    print(query_client.service.query_by_name(request['title']))
  elif (type=='query_by_author'):
    print("\n=======query_by_author on %s , result is========\n"%request['name'])
    print(query_client.service.query_by_author(request['name']))
  elif (type=='query_keywords'):
    print("\n=======query_keywords on %s , result is========\n"%str(request['keywords']))
    import pickle
    args = pickle.dumps(request['keywords'])
    print(query_client.service.query_keywords(args))
  elif (type=='query_coop_by_names'):
    print("\n=======query_coop_by_names on %s AND %s , result is========\n"\
          %(request['name1'],request['name2']))
    print(query_client.service.query_coop_by_names(request['name1'],request['name2']))
  