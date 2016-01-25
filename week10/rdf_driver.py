"""
Service Oriented Computing Lab Week10 in Python.
DBLP on RDF

RDF Driver class
Store DBLP data to RDF
Query RDF
Store to RDF file

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    11/8/2015
"""
import rdflib
from rdflib import Namespace, BNode, Literal


class RDFDriver:
    """
    RDF Driver Class
    """
    dblpns = Namespace("Http://localhost/dblp/")

    def __init__(self):
        """
        Init the graph
        :return:
        """
        self.graph = rdflib.Graph()

    def add_documents(self, d):
        """
        Add a list of publications to the RDF graph
        :param d: List of documents
        :return:
        """
        for i in d:
            self.add_entry(i)

    def add_entry(self, entry):
        """
        Add a DBLP entry to the graph
        For author, create a seq to hold multiple authors
        :param entry: A DBLP Entry
        :return:
        """
        s = BNode()
        for k, v in entry.items():
            if k == "author":
                o = rdflib.BNode()
                p = self.dblpns.__getitem__(k)
                self.graph.add( (s, p, o) )
                self.graph.add((o, rdflib.RDF.type, rdflib.RDF.Seq))
                index = 1
                for author in v:
                    self.graph.add((o, rdflib.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#_%s' % index),
                                    Literal(author)))
                    index += 1
            else:
                p = self.dblpns.__getitem__(k)
                o = Literal(v)
                self.graph.add( (s, p, o) )

    def parse(self, rdf_file):
        """
        Parse an RDF file
        :param rdf_file: RDF File Path
        :return:
        """
        self.graph.parse(rdf_file)

    def serialize(self, fileout):
        """
        Store the graph to an RDF file
        :param fileout: Output file path
        :return:
        """
        self.graph.serialize(fileout, "xml")

    def query_by_title(self, name):
        """
        Query The RDF graph using publication title
        :param name: The title of the publication
        :return: List of the details of the result publication
        """
        query =\
"""SELECT DISTINCT ?title ?url ?year ?key ?ee
WHERE {
      ?a ns:title ?title .
      filter CONTAINS(?title, "%s") .
      ?a ns:url ?url .
      ?a ns:year ?year .
      ?a ns:key ?key .
      ?a ns:ee ?ee .
      }""" % name
        res = self.graph.query(query, initNs={ 'ns': self.dblpns })
        return res

    def query_coauthor(self, author):
        """
        Query the graph using an author's name.
        Find the co-authors and their cooperate publications
        :param author: The author's name
        :return: List of the title of the publication and the name of the co-author
        """
        query =\
"""SELECT DISTINCT ?title ?author
WHERE {
        ?a ns:title ?title .
        ?a ns:author ?authors .
        ?authors ?t2 ?statement.
        filter CONTAINS(?statement, "%s") .
        ?a ns:author ?authors2 .
        ?authors2 ?t ?author .
        filter CONTAINS(?author, ?author) .
        filter (?author != "%s") .
        }""" % (author, author)
        res = self.graph.query(query, initNs={ 'ns': self.dblpns })
        return res
