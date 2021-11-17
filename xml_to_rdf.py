# Convert XML to RDF 
# Inputs: data xml file with specific xml schema
from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys


# When calling this script enter script.py filename record schema1 schema2 ... schema_n
def main():
    if sys.argv:
        filename = sys.argv[1]
        schemas = []
        record_name = sys.argv[2]

        for i in range(3, len(sys.argv):
            schemas.append(sys.argv[i])

    else:
        filename = 'data/geoportal_search.xml'
        schemas = ['dc:subject', 'dct:references']
        record_name = 'csw:Record'

    content = []

    with open(filename, 'r') as page:
        content = page.readlines()
        content = ''.join(content)
        bs_content = BeautifulSoup(content,'lxml')

    # Parse through the xml file

    # Write RDF file

    # Save RDF file

main()
