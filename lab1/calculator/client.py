#!/usr/bin/env python
"""
Service Oriented Computing Week1 Lab
Client example

Using suds to consume wsdl and call the service.

Usage: 
python client.py [-a IP] [-p PORT] op1 OPR op2
or use -h to view help message

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    9/6/2015
"""

from suds.client import Client
from argparse import ArgumentParser
import logging

if __name__=='__main__':
  logging.getLogger().setLevel(logging.INFO)
  parser = ArgumentParser(description='Calculator arguments.')
  parser.add_argument('-a', metavar='IP', default='', 
                      help='ip listened.')
  parser.add_argument('-p', metavar='PORT', type=int,
                      help='port listened')
  parser.add_argument('op1', type=int, 
                      help='first operand')
  parser.add_argument('O',  type=str, 
                      help='operations including ADD SUB MUL DIV')
  parser.add_argument('op2', type=int, 
                      help='second operand')
  po = parser.parse_args()
  
  address = 'localhost' if len(po.a)==0 else po.a
  address = ':'.join([address, str(po.p)])
  
  calculator_client = Client('http://%s/?wsdl' % address)
  
  operations={
              'ADD':calculator_client.service.add,
              'SUB':calculator_client.service.minus,
              'MUL':calculator_client.service.multiply,
              'DIV':calculator_client.service.divide
              }
  
  try:
    print(operations[po.O.upper()](po.op1, po.op2))
  except KeyError:
    raise Exception('Wrong operation, use ADD SUB MUL DIV')
  