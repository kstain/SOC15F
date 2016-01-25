#!/user/bin/env python
"""
Service Oriented Computing Week2 Lab
Data truncator for dblp dataset

Usage: 
from xml_truncate import trunc
trunc(count=count, fin=in_path, fout=out_path)

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    9/13/2015
"""

def trunc(count=1000,fin='data/dblp.xml', fout='data/dblp_t.xml'):
  def getKeyTag():
    while(1):
      yield '<article'
      yield '</article'
  with open(fin, 'r') as fin:
    with open(fout, 'w') as fout:
      keygen = getKeyTag()
      entryCount = 0
      while (entryCount < 2*count):
        currentKey = next(keygen)
        line = fin.readline()
        while (currentKey not in line):
          if (len(line.strip())!=0):
            fout.write(line)
          line = fin.readline()
        fout.write(line)
        entryCount+=1
      fout.write('</dblp>')
      
if __name__=='__main__':
  trunc()