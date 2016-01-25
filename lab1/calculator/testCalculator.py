"""
Testcase for SOC calculator

Usage:
nosetests testCalculator.py
"""
from calculator import CalculatorService, Application, Soap11, WsgiApplication, make_server, WSGIRequestHandler
from client import Client
from nose.tools import with_setup
import logging
import threading

def setup_module():
  """
  The fixture is to set up the server and client.
  """
  app = Application([CalculatorService], 'soc.week1.calculator',
                    in_protocol=Soap11(validator='lxml'),
                    out_protocol=Soap11(),
  )
  wsgi_app = WsgiApplication(app)
  class NoLoggingWSGIRequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        pass
  server = make_server('', 10009, wsgi_app, handler_class=NoLoggingWSGIRequestHandler)
  t = threading.Thread(target=server.serve_forever)
  t.setDaemon(True)
  t.start()
  global calculator_client
  calculator_client = Client('http://localhost:10009/?wsdl')
 
def teardown_module():
    pass

class TestCalculator():
  """
  Test class for calculator web service.
  Calculate four operations and check the result.
  """
  def test_add_1(self):
    """
    There are some unpredicable behavior or ..bugs? in suds
    And there is a discussion there
    https://github.com/nose-devs/nose/issues/795
    Have to set logging level separately to walkaround the problem.
    """
    logging.getLogger().setLevel(logging.INFO)
    assert calculator_client.service.add(1,4)==5
  def test_add_2(self):
    logging.getLogger().setLevel(logging.INFO)
    assert calculator_client.service.add(-1,-4)==-5
  def test_sub_1(self):
    logging.getLogger().setLevel(logging.INFO)
    assert calculator_client.service.minus(10,4)==6
  def test_sub_2(self):
    logging.getLogger().setLevel(logging.INFO)
    assert calculator_client.service.minus(1,-4)==5
  def test_mul_1(self):
    logging.getLogger().setLevel(logging.INFO)
    assert calculator_client.service.multiply(-1,-4)==4
  def test_mul_2(self):
    logging.getLogger().setLevel(logging.INFO)
    assert calculator_client.service.multiply(-1,4)==-4
  def test_div_1(self):
    logging.getLogger().setLevel(logging.INFO)
    assert calculator_client.service.divide(-1,4)==-1
  def test_div_2(self):
    logging.getLogger().setLevel(logging.INFO)
    assert calculator_client.service.divide(-1,0)==None