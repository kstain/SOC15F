# SOC LAB10
Name: Weiyi Wang
Andrew ID: weiyiw

## Description
This lab is written in python and based on [RDFLib](https://rdflib.readthedocs.org).

RDF format file storage and query of "publication title query" and "co-author query" are completed.

## How to run
### Environment
1. Install RDFLib using
> pip install rdflib
2. Test python environment using the follow command in python. If the error occurs, congrats.
> import rdflib

### Run the example
> python example.py

The example python file will load 100 entries from the DBLP xml file and store it in RDF triples.

On level 1, query on publication title will be performed.

On level 2, the RDF will be converted to RDF file on local disc. Check DBLPRDF.xml to exam the file.
Then query on co-author will be performed.

## Implementation Description

### Level 1

The parser of DBLP in lab2 is reused in this lab. There are minor changes to the parser to adapt output format.

In the RDFDriver class, publication data from the parser is dissembled to construct the triples used in
storing to RDF format.

For each triple of (s, p, o):
* s stands for the document node
* p is the type of the data, e.g. title
* o is the value of the type, e.g. "On Parallel Integer Sorting."

For author type, an rdf:seq node is created and the authors are applied to that sequence.

#### Query on title
The query of rdf is based on SPARQL.

To get the details based on the title, the following is the query code:
```
SELECT DISTINCT ?title ?url ?year ?key ?ee
WHERE {
      ?a ns:title ?t .
      filter CONTAINS(?t, TITLE_OF_THE_PUBLICATION) .
      ?a ns:url ?url .
      ?a ns:year ?year .
      ?a ns:key ?key .
      ?a ns:ee ?ee .
      }
```

### Level 2

#### RDF file storage
This feature is based on [serialize](http://rdflib.readthedocs.org/en/latest/apidocs/rdflib.html?highlight=serialize#rdflib.graph.Graph.serialize) function of RDFLib.

#### Query on co-author
The seq of author is coped with the following SPARQL query:
```
SELECT DISTINCT ?title ?author
WHERE {
        ?a ns:title ?title .
        ?a ns:author ?authors .
        ?authors ?t2 ?statement.
        filter CONTAINS(?statement, NAME_OF_THE_AUTHOR) .
        ?a ns:author ?authors2 .
        ?authors2 ?t ?author .
        filter CONTAINS(?author, ?author) .
        filter (?author != NAME_OF_THE_AUTHOR) .
        }
```
First find the publications whose author is the given one. Then find the other different authors in that publication.


