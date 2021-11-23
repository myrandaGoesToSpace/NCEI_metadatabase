# Convert XML to RDF 
# Inputs: data xml file with specific xml schema
from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys

def get_attr(soup, attr_name):
    attr_list = []
    attr_character_string = soup.find_all(attr_name)
    
    for attr in attr_character_string:
        attr_list.append(attr.text)

    return attr_list

# When calling this script enter script.py filename record schema1 schema2 ... schema_n
# Default is CSW and Dublin Core (dc)

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        schemas = []
        record_name = sys.argv[2]

        for i in range(3, len(sys.argv)):
            schemas.append(sys.argv[i])

    else:
        filename = 'data/geoportal_search.xml'
        schemas = ['dc:subject']
        record_name = 'csw:record'

    content = []

    with open(filename, 'r') as page:
        content = page.readlines()
        content = ''.join(content)
        soup = BeautifulSoup(content,'lxml')
    
    # Test
    #print("soup file:")
    #print(soup)

    # Parse through the xml file
    records = []
    subjects = []
    attrs = []
    
    # TO DO: EXPAND TO SEARCH FOR MANY ATTRIBUTES AND ADD THEM TO DICTIONARY    
    #print('records')
    #print(soup.find_all(record_name))

    for record in soup.find_all(record_name):
        attrs.append(get_attr(record, schemas[0]))

        # Test
        print('soup found: ')
        print(get_attr(soup, schemas[0]))
        
    # Create dictionary
    metadata_dict = {}

    for schema in schemas:
        metadata_dict[schema] = attrs
        
        # Testing
        print('dictionary:')
        print(metadata_dict[schema])

    # Write RDF file
    metadata_df = pd.DataFrame(metadata_dict)
    
    # Test
    print('df:')
    print(metadata_df)

    PATH = filename
    PATH = PATH.replace('xml','csv')
    
    # Test
    print('path to save:')
    print(PATH)

    metadata_df.to_csv(PATH)

    # Save RDF file

main()
