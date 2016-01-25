#!/usr/bin/env python
"""
Service Oriented Computing Lab Week3 in Python.
Transformer service using spyne
Client part.

python client.py [-a IP] -p PORT -f XML_FILE
or use -h to view help message

If -a is omitted the server will listen to all IPs
listed.

Use suds to call the service.
Code example is in client.py

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    9/18/2015
"""

from suds.client import Client
from argparse import ArgumentParser
import pickle

parser = ArgumentParser(description='Code Generator arguments.')
parser.add_argument('-a', metavar='IP', default='', 
                    help='ip listened.')
parser.add_argument('-p', metavar='PORT', type=int,
                    help='port listened')
parser.add_argument('-f', metavar='FILE', type=str,
                    help='class XML file')
po = parser.parse_args()

  
address = 'localhost' if len(po.a)==0 else po.a
address = ':'.join([address, str(po.p)])

query_client = Client('http://%s/?wsdl' % address)

with open(po.f) as f:
  request=f.read()
  
print(query_client.service.generate(request))
  