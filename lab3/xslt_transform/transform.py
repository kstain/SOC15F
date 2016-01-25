#!/usr/bin/env python
"""
Service Oriented Computing Lab Week3 in Python.
The transformer code for python class code generation.
Output will be stdout.

Usage:

python transform.py XML_FILE XSLT_FILE

@author:  Weiyi Wang
@contact: weiyi.wang@sv.cmu.edu
@date:    9/6/2015
"""

from lxml import etree
import sys

xml = etree.parse(sys.argv[1])
xslt = etree.parse(sys.argv[2])
transform = etree.XSLT(xslt)
code = transform(xml)
print(bytes(code))