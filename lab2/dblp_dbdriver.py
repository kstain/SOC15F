#!/user/bin/env python
"""
Service Oriented Computing Lab Week2 in Python.
DBLP Query service On Web

Database Class for DBLP

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    9/13/2015
"""

import MySQLdb
import logging
import sys

class DBLPDatabaseDriver:
  """
  Dababase Driver for data storing and querying
  """
  _instance = None

  _host = None
  _username = None
  _password = None
  _database = None

  _cursor = None
  _connection = None

  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super(Mysql, cls).__new__(cls, *args, **kwargs)
    return cls._instance
    
  def __del__(self):
    self._close()

  def __init__(self, host='localhost', username='root', 
               password='', database='', create_db_on_start=False):
    self._host = host
    self._username = username
    self._password = password
    self._database = database
    self._open(create_db_on_start)
      
  def _open(self, create):
    try:
      if create:
        self._connection = MySQLdb.connect(self._host, 
                                           self._username, 
                                           self._password,
                                           charset='utf8')
        self._cursor = self._connection.cursor(MySQLdb.cursors.DictCursor)
        query = 'CREATE DATABASE IF NOT EXISTS ' + self._database
        self._cursor.execute(query)
        query = 'USE ' + self._database
        self._cursor.execute(query)
      else:
        self._connection = MySQLdb.connect(host=self._host,
                                           user=self._username, 
                                           passwd=self._password,
                                           charset='utf8',
                                           db=self._database)
        self._cursor = self._connection.cursor(MySQLdb.cursors.DictCursor)
    except MySQLdb.Error as err:
      print('Error: %s ' %err)
      sys.exit()

  def _close(self):
    self._cursor.close()
    self._connection.close()
      
  @property
  def execute(self):
    return self._cursor.execute
      
  def create_table(self, on_dirty=False):
    """
    Create two tables.
    if on_dirty, will not create if there exists
    those tables in db
    """
    if (on_dirty==False):
      try:
        query='''
DROP TABLE Authors;
'''
        self.execute(query)
        query='''
DROP TABLE Publications;
'''
        self.execute(query)
        self._connection.commit()
      except:
        pass
        
    query='''
CREATE TABLE IF NOT EXISTS Publications
(
ID INT NOT NULL AUTO_INCREMENT,
Pub_type varchar(15) NOT NULL,
Pub_editor varchar(100) ,
Pub_title varchar(200),
Pub_booktitle varchar(100),
Pub_pages varchar(100),
Pub_year INT,
Pub_address varchar(100),
Pub_journal varchar(100),
Pub_volume varchar(100),
Pub_number varchar(100),
Pub_month varchar(100),
Pub_url varchar(100),
Pub_ee varchar(100),
Pub_cdrom varchar(100),
Pub_cite varchar(100),
Pub_publisher varchar(100),
Pub_note varchar(100),
Pub_crossref varchar(100),
Pub_isbn varchar(100),
Pub_series varchar(100),
Pub_school varchar(100),
Pub_chapter varchar(100),

Pub_key varchar(100),
Pub_mdate varchar(100),
Pub_publtype varchar(100),
Pub_reviewid varchar(100),
Pub_rating varchar(100),
PRIMARY KEY (ID)
);
'''
    self.execute(query)
    query='''
CREATE TABLE IF NOT EXISTS Authors
(
Name varchar(100) NOT NULL,
Pub_ID INT NOT NULL,
FOREIGN KEY (Pub_ID) REFERENCES Publications(id)
);
'''
    self.execute(query)
    query='''
CREATE TABLE IF NOT EXISTS PublicationsSpatial
(
year POINT NOT NULL,
Pub_ID INT NOT NULL,
FOREIGN KEY (Pub_ID) REFERENCES Publications(id),
SPATIAL INDEX(year)
) ENGINE=MyISAM;
'''
    self.execute(query)
    
  def insert_entry(self, pub_dict):
    authors = pub_dict.pop('Pub_author')
    keys = ', '.join(pub_dict.keys())
    escaped = []
    for value in pub_dict.values():
      if isinstance(value,str):
        value = value.replace('"','\\"')
      elif (value==None):
        value=''
      escaped.append(value)
    values = '"' + '", "'.join(escaped) + '"'
    query = '''
INSERT INTO Publications (%s)
VALUES (%s);
''' % (keys, values)
    self.execute(query)
    id = self._cursor.lastrowid
    for author in authors:
      query = '''
INSERT INTO Authors (Name, Pub_ID)
VALUES ("%s",%s);
''' % (author, str(id))
      self.execute(query)
    year = pub_dict['Pub_year']
    query = '''
INSERT INTO PublicationsSpatial (year, Pub_ID)
VALUES (GeomFromText('POINT(%s 1)'),%s);
''' % (year, str(id))
    self.execute(query)
  
  def commit(self):
    self._connection.commit()  
    
  def rinse(self, results):
    """
    Pick out all None Fields
    """
    is_dict = isinstance(results, dict)
    if is_dict:
      results=[results,]
    for entry in results:
      for k,v in entry.items():
        if (v==None):
          entry.pop(k)
    return results[0] if is_dict else results

  def get_all_docs(self):
    """
    Fetch all the documents
    """
    query='''
select * from Publications;
'''
    self.execute(query)
    resultSet = self._cursor.fetchall()
    for result in resultSet:
      result['Pub_author'] = []
      pid = result['ID']
      query='''
select Name from Authors where Pub_ID=%s;
''' % str(pid)
      self.execute(query)
      authors = self._cursor.fetchall()
      for author in authors:
        result['Pub_author'].append(author)
    return self.rinse(resultSet)
    
    
  def query_by_id(self,id):
    """
    Fetch publication details using ID
    """
    query='''
select * from Publications where ID=%s;
''' % id
    self.execute(query)
    resultSet = self._cursor.fetchall()
    for result in resultSet:
      result['Pub_author'] = []
      pid = result['ID']
      query='''
select Name from Authors where Pub_ID=%s;
''' % str(pid)
      self.execute(query)
      authors = self._cursor.fetchall()
      for author in authors:
        result['Pub_author'].append(author)
    return self.rinse(resultSet)
        
  
  def query_by_name(self, name):
    """
    Query publication details using title
    """
    query='''
select * from Publications where Pub_title like "%%%s%%";
''' % name
    self.execute(query)
    resultSet = self._cursor.fetchall()
    for result in resultSet:
      result['Pub_author'] = []
      pid = result['ID']
      query='''
select Name from Authors where Pub_ID=%s;
''' % str(pid)
      self.execute(query)
      authors = self._cursor.fetchall()
      for author in authors:
        result['Pub_author'].append(author)
    return self.rinse(resultSet)
  
  def query_coauthor(self, name):
    """
    Querying all ao-author using author's name
    """
    coauthors = set()
    query='''
select Pub_ID from Authors where Name like "%%%s%%";
''' % name
    self.execute(query)
    results = self._cursor.fetchall()
    for entry in results:
      id = entry['Pub_ID']
      query='''
select Name from Authors where Name not like "%%%s%%" and Pub_ID=%s;
''' % (name, str(id))
      self.execute(query)
      ca_results = self._cursor.fetchall()
      for ca_result in ca_results:
        coauthors.add(ca_result['Name'])
    return coauthors
    
  def query_by_author(self, name):
    """
    Query publication details using author's name
    """
    query='''
select Pub_ID from Authors where Name like "%%%s%%";
''' % name
    self.execute(query)
    pub_results = self._cursor.fetchall()
    detail_list = []
    for entry in pub_results:
      id = entry['Pub_ID']
      query='''
select * from Publications where ID=%s;
''' % (str(id))
      self.execute(query)
      results = self._cursor.fetchall()
      for result in results:
        result['Pub_authors']=[name]
        pid = result['ID']
        query='''
select Name from Authors where Name not like "%%%s%%" and Pub_ID=%s;
''' % (name, str(pid))
        self.execute(query)
        ca_results = self._cursor.fetchall()
        for ca in ca_results:
          result['Pub_authors'].append(ca['Name'])
        detail_list.append(result)
    return self.rinse(detail_list)
    
  def query_keywords(self, keyword_list):
    """
    List all publications that contain 
    some or all of the keywords in the paper title.
    """
    query_piece=''
    if len(keyword_list)==1:
      query_piece="Pub_title like '%%%s%%'" % keyword_list[0]
    elif (len(keyword_list)>1):
      query_piece="Pub_title like '%%%s%%'" % keyword_list[0]
      for entry in keyword_list[1:]:
        query_piece=' OR '.join([query_piece, "Pub_title like '%%%s%%'"%entry])
    else:
      raise Exception('Bad Argument')
    query='''
select * from Publications 
where %s;
''' % query_piece
    self.execute(query)
    resultSet = self._cursor.fetchall()
    for result in resultSet:
      result['Pub_author'] = []
      pid = result['ID']
      query='''
select Name from Authors where Pub_ID=%s;
''' % str(pid)
      self.execute(query)
      authors = self._cursor.fetchall()
      for author in authors:
        result['Pub_author'].append(author)
    return self.rinse(resultSet)
    
  def query_coop_by_names(self, name1, name2):
    """
    Query two authors' co-works
    """
    query='''
select t1.Pub_ID 
from Authors t1 left outer join Authors t2 on t1.Pub_ID = t2.Pub_ID 
where t1.Name = "%s" and t2.name = "%s";
''' % (name1, name2)
    self.execute(query)
    pids = self._cursor.fetchall()
    if len(pids)==0:
      return None
    detail_list = []
    for pid in pids:
      detail_list.append(self.query_by_id(pid['Pub_ID'])[0])
    return detail_list
    
  class YearInterval:
    def __init__(self, start, end):
      if start>end:
        raise Exception("Wrong year interval definition!")
      self.start = start
      self.end = end

    def to_polygen(self):
      return 'Polygon((%s 0, %s 0, %s 2, %s 2, %s 0))' % (str(self.start),str(self.end),str(self.end),str(self.start),str(self.start))
  
  def query_by_year(self, yearInterval):
    query='''
SET @poly =
'%s';
''' % yearInterval.to_polygen()
    self.execute(query)
    query='''   
select Pub_ID
from PublicationsSpatial
where MBRContains(GeomFromText(@poly),year);
'''
    self.execute(query)
    pids = self._cursor.fetchall()
    if len(pids)==0:
      return None
    detail_list = []
    for pid in pids:
      detail_list.append(self.query_by_id(pid['Pub_ID'])[0])
    return detail_list

    