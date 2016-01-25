#!/usr/bin/env python
"""
Service Oriented Computing Lab Week1 in Python.
Calculator service using spyne to generate a server
and create a service client.

Usage to start the service

python calculator.py [-a IP] -p PORT
or use -h to view help message

If -a is omitted the server will listen to all IPs
listed.

Use suds to call the service.
Code example is in client.py

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    9/6/2015
"""

import spyne
from spyne.application import Application
from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.primitive import Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class CalculatorService(ServiceBase):
  """
  Service class which implements the operations
  """
  @srpc(Integer, Integer, _returns=Integer)
  def add(op1, op2):
    return op1+op2
  @srpc(Integer, Integer, _returns=Integer)
  def minus(op1, op2):
    return op1-op2
  @srpc(Integer, Integer, _returns=Integer)
  def multiply(op1, op2):
    return op1*op2
  @srpc(Integer, Integer, _returns=Integer)
  def divide(op1, op2):
    """
    Divide the two operands and round the result to int
    Return None when divided by zero
    """
    try:
      return op1/op2
    except ZeroDivisionError:
      return None
    
    
from wsgiref.simple_server import make_server, WSGIRequestHandler
from argparse import ArgumentParser
import logging

if __name__=='__main__':
  logging.getLogger().setLevel(logging.INFO)
  parser = ArgumentParser(description='Calculator arguments.')
  parser.add_argument('-a', metavar='IP', default='', 
                      help='ip listened.')
  parser.add_argument('-p', metavar='PORT', type=int, 
                      help='port listened')
  po = parser.parse_args()

  app = Application([CalculatorService], 'soc.week1.calculator',
      in_protocol=Soap11(validator='lxml'),
      out_protocol=Soap11(),
  )
  wsgi_app = WsgiApplication(app)
  server = make_server(po.a, po.p, wsgi_app)
  
  address = 'localhost' if len(po.a)==0 else po.a
  address = ':'.join([address, str(po.p)])

  print("listening to http://%s"%address)
  print("wsdl is at: http://%s/?wsdl"%address)

  server.serve_forever()