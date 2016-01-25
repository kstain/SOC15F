#!/user/bin/env python#!/user/bin/env python
"""
Service Oriented Computing Lab Week2 in Python.
DBLP Query service On Web

XMLParser for DBLP dataset
Parse the xml, store in Python structures,
and push to DB driver

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    9/13/2015
"""

from lxml import etree
import sys

class DBLPParser():
  def __init__(self, xml_path, base_path=None):
    """
    Parse the xml against DTD
    """
    parser = etree.XMLParser(load_dtd=True)
    try:
      self.tree = etree.parse(xml_path, parser)
    except:
      self.tree = None
    self.pub_list = []
  
  @property
  def root(self):
    return self.tree.getroot()
    
  def visit(self):
    """
    Tour the root and store in pythonic structures
    """
    for child in self.root:
      pub_dict = {'Pub_type':child.tag, 'Pub_author':[]}
      attrib = child.attrib
      for k,v in child.items():
        pub_dict['Pub_'+k] = v
      for element in child:
        if element.tag=='author':
          pub_dict['Pub_author'].append(element.text)
        else:
          pub_dict['Pub_'+element.tag] = element.text
      self.pub_list.append(pub_dict)
  
  def push_to_db(self, db):
    """
    Push the data to database driver
    """
    if (db==None):
      raise Exception('DataBase is not initialized')
    counter = 0
    for item in self.pub_list:
      db.insert_entry(item)
      counter+=1
      if (counter%50==0):
        sys.stderr.write('\r%s%% records inserted!'%str(counter*100/len(self.pub_list)))
        sys.stderr.flush()
    sys.stderr.write('\rAll records inserted!')
    sys.stderr.flush()    
    db.commit()