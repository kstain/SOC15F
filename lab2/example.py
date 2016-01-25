#!/user/bin/env python
"""
Service Oriented Computing Week2 Lab
Client example (NO WEB SERVICE)

Please fill the information of database before use!

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    9/13/2015
"""

import yaml

config = {}
with open('config.yaml', 'r') as stream:
  config=(yaml.load(stream))
  
PASSWORD= config['password']
DATABASE=config['database']
HOST=config['host']
USERNAME=config['username']

from dblp_dbdriver import DBLPDatabaseDriver
from dblp_parser import DBLPParser

import pprint

db = DBLPDatabaseDriver(host=HOST,password=PASSWORD, 
                        database=DATABASE, 
                        username=USERNAME,
                        create_db_on_start=False)
db.create_table()

parser = DBLPParser(config['xmlpath'])
parser.visit()
parser.push_to_db(db)

print('\n\n----------Listing Co-Authors-------------')
pprint.pprint(db.query_coauthor('Eike Best'))

print('\n\n----------Querying by title-------------')
pprint.pprint(db.query_by_name('Extended multi bottom-up tree transducers.'))

print('\n\n----------Querying by author-------------')
pprint.pprint(db.query_by_author('Eike Best'))

print('\n\n----------Querying by keywords-------------')
pprint.pprint(db.query_keywords(['multi', 'space']))

print('\n\n----------Querying by two authors-------------')
pprint.pprint(db.query_coop_by_names('Andreas Maletti','Eric Lilin'))

