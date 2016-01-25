#!/usr/bin/env python
"""
Service Oriented Computing Lab Week3 in Python.
Transformer service using spyne
Method generate(String) can be called to consume an xml file
and generate python code for the class described in the xml.
Usage to start the service

python server.py [-a IP] -p PORT -x XSLT_FILE
or use -h to view help message

If -a is omitted the server will listen to all IPs
listed.

Use suds to call the service.
Code example is in client.py

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    9/18/2015
"""
from lxml import etree

import spyne
from spyne.application import Application
from spyne.decorator import rpc
from spyne.service import ServiceBase
from spyne.model.primitive import String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class MyApplication(Application):
    def __init__(self, *args, **kargs):
      xslt_path = kargs.pop('_xslt')
      Application.__init__(self, *args, **kargs)
      xslt = etree.parse(xslt_path)
      self.transform = etree.XSLT(xslt)
   
class CodeGenService(ServiceBase):
  @rpc(String,  _returns=String)
  def generate(ctx, xml):
    from io import BytesIO
    ori = BytesIO(xml)
    try:
      code = ctx.app.transform(etree.parse(ori))
    except:
      return 'Cannot transform the xml, please check.'
    return bytes(code)
      
from wsgiref.simple_server import make_server
from argparse import ArgumentParser

if __name__=='__main__':
  parser = ArgumentParser(description='Code Generator arguments.');
  parser.add_argument('-a', metavar='IP', default='', 
                      help='ip listened.');
  parser.add_argument('-p', metavar='PORT', type=int, 
                      help='port listened');
  parser.add_argument('-x', metavar='XSLT', type=str, 
                      help='xslt file');
  po = parser.parse_args();

  app = MyApplication([CodeGenService], 'soc.week3.CodeGenService',
                      _xslt = po.x,
                      in_protocol=Soap11(validator='lxml'),
                      out_protocol=Soap11(),
  );
  
  wsgi_app = WsgiApplication(app);
  server = make_server(po.a, po.p, wsgi_app);
  
  address = 'localhost' if len(po.a)==0 else po.a;
  address = ':'.join([address, str(po.p)]);

  print("listening to http://%s"%address);
  print("wsdl is at: http://%s/?wsdl"%address);

  server.serve_forever();