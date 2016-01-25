"""
Service Oriented Computing Lab Week10 in Python.
DBLP on RDF

DBLP Parser class
Parse DBLP to python data structure

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    11/8/2015
"""
from lxml import etree


class DBLPParser:
    """
    DBLP Parser
    """
    def __init__(self, xml_path, base_path=None):
        """
        Parse the xml against DTD
        :param xml_path: The xml file path
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
            pub_dict = {'type':child.tag, 'author':[]}
            attrib = child.attrib
            for k,v in child.items():
                pub_dict[k] = v
            for element in child:
                if element.tag=='author':
                    pub_dict['author'].append(element.text)
                else:
                    pub_dict[element.tag] = element.text
            self.pub_list.append(pub_dict)

    @property
    def publications(self):
        return self.pub_list
