#!/usr/bin/env python
"""
Service Oriented Computing Lab Week2 in Python.
DBLP Query service On Web

Usage: 
python service.py [-a IP] [-p PORT] -c FILE
or use -h to view help message

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    9/13/2015
"""

import spyne
from spyne.application import Application
from spyne.decorator import srpc, rpc
from spyne.service import ServiceBase
from spyne.model.primitive import Integer
from spyne.model.primitive import String
from spyne.protocol.soap import Soap11
from spyne import Iterable, Array
from spyne.server.wsgi import WsgiApplication

from dblp_dbdriver import DBLPDatabaseDriver
from dblp_parser import DBLPParser

class MyApplication(Application):
    def __init__(self, *args, **kargs):
      password = kargs.pop('_mypassword')
      host = kargs.pop('_myhost')
      username = kargs.pop('_username')
      database = kargs.pop('_database')
      xml_path = kargs.pop('_xmlpath')
      Application.__init__(self, *args, **kargs)
      assert not hasattr(self, '_password')
      assert not hasattr(self, '_host')
      assert not hasattr(self, '_username')
      self._db=DBLPDatabaseDriver(host=host,
                                  username=username,
                                  password=password,
                                  database=database,
                                  create_db_on_start=True)
      self._db.create_table()
      parser = DBLPParser(xml_path)
      parser.visit()
      parser.push_to_db(self._db)
        

class DBLPLookupService(ServiceBase):
  @rpc(String,  _returns=Iterable(String))
  def query_coauthor(ctx, name):
    return list(ctx.app._db.query_coauthor(name))
    
  @rpc(String, _returns=Iterable(String))
  def query_by_name(ctx, name):
    response = []
    result = ctx.app._db.query_by_name(name)
    for each in result:
      response.append(str(each))
    return response
    
  @rpc(String, _returns=Iterable(String))
  def query_by_author(ctx, name):
    response = []
    result = ctx.app._db.query_by_author(name)
    for each in result:
      response.append(str(each))
    return response
    
  @rpc(String, _returns=Iterable(String))
  def query_keywords(ctx, name):
    import pickle
    keywords=pickle.loads(name)
    response = []
    result = ctx.app._db.query_keywords(keywords)
    for each in result:
      response.append(str(each))
    return response
    
  @rpc(String, String, _returns=Iterable(String))
  def query_coop_by_names(ctx, name1, name2):
    response = []
    result = ctx.app._db.query_coop_by_names(name1, name2)
    for each in result:
      response.append(str(each))
    return response
    
  
from wsgiref.simple_server import make_server
from argparse import ArgumentParser
import yaml

if __name__=='__main__':
  parser = ArgumentParser(description='Server arguments.');
  parser.add_argument('-a', metavar='IP', default='', 
                      help='ip listened.');
  parser.add_argument('-p', metavar='PORT', type=int, 
                      help='port listened');
  parser.add_argument('-c', metavar='CFG', type=str, 
                      help='configure file');
  po = parser.parse_args();
  
  config = {}
  with open(po.c, 'r') as stream:
    config=(yaml.load(stream))

  app = MyApplication([DBLPLookupService], 'soc.week2.DBLPService',
      in_protocol=Soap11(validator='lxml'),
      out_protocol=Soap11(),
      _mypassword = config['password'],
      _myhost = config['host'],
      _username = config['username'],
      _database = config['database'],
      _xmlpath = config['xmlpath']
  );
  
  wsgi_app = WsgiApplication(app);
  server = make_server(po.a, po.p, wsgi_app);
  
  address = 'localhost' if len(po.a)==0 else po.a;
  address = ':'.join([address, str(po.p)]);

  print("listening to http://%s"%address);
  print("wsdl is at: http://%s/?wsdl"%address);

  server.serve_forever();