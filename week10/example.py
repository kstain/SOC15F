"""
Service Oriented Computing Lab Week10 in Python.
DBLP on RDF

Example usage

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    11/8/2015
"""
from dblp_parser import DBLPParser
from rdf_driver import RDFDriver


"""
Level 1: Load DBLP data to RDFLib and do simple query
given a publication name, list its detailed information
"""
print("=========LEVEL 1========")
parser = DBLPParser("data/dblp_t100.xml")
parser.visit()  # Parse the data and store in python

print("Converting to rdf data..\n")
driver = RDFDriver()
driver.add_documents(parser.publications)  # Store the data to RDF format

print("Querying the detail of publication 'On Parallel Integer Sorting'")
res = driver.query_by_title('On Parallel Integer Sorting')
for row in res:
    print row

"""
Level 2:  turn the DBLP (XML) into RDF format, add query like
given author A, provide all of her co-authors together with the corresponding publication information
"""
print("\n\n=========LEVEL 2========")
print("Store the data to DBLPRDF.xml")
driver.graph.serialize("DBLPRDF.xml", "xml")  # Check the file to see the result

print("Querying co-author information of 'Ivan Hal Sudborough'")
res = driver.query_coauthor("Ivan Hal Sudborough")
for row in res:
    print row
