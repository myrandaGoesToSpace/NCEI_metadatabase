# Script to get metadata from Geoportal

from bs4 import BeautifulSoup
import pandas as pd
import sys
import requests

def get_attr(soup, attr_name):
    attr_list = []
    attr_character_string = soup.find_all(attr_name)

    for attr in attr_character_string:
        attr_list.append(attr.text)

    return attr_list

def main():
    num_results = 10
    URL = "https://www.ncei.noaa.gov/metadata/geoportal/opensearch?f=csw&from=0&size=" + str(num_results)
    filename = "data/parsed_metadata.xml"

    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "lxml")

    schemas = ['dc:subject']
    record_name = 'csw:record'
    identifier = 'dc:identifier'    
    
    # Parse through the xml file
    metadata_dict = {}
    id_list = []

    for i in range(len(schemas)):
        attrs = []
        for record in soup.find_all(record_name):
            attrs.append(get_attr(record, schemas[i]))

            if i == 0:
                id_list.append(get_attr(record, identifier))
                metadata_dict['identifier'] = id_list

        metadata_dict[schemas[i]] = attrs
        # Test
        print('soup found: ')
        print(get_attr(soup, schemas[i]))
    
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

    # Necessary variables
    PATH = filename
    PATH = PATH.replace('.xml','_rdf.xml')

    # Dictionary to hold xml schemas
    xml_schema_terms = {}

    xml_schema_terms['header'] = "<?xml version = '1.0' encoding='UTF-8' ?>"
    xml_schema_terms['rdf'] = "xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' "
    xml_schema_terms['dc'] = "xmlns:dc='http://purl.org/dc/elements/1.1/' "
    xml_schema_terms['dct'] = "xmlns:dct='http://purl.org/dc/terms/' "
    xml_schema_terms['rdfs'] = "xmlns:rdfs='http://www.w3.org/TR/2014/REC-rdf-schema-20140225/'"

    schemas_to_include = [xml_schema_terms['rdf'], xml_schema_terms['rdfs']]

    for schema in schemas:
        for key in xml_schema_terms.keys():
            if schema.startswith(key) and xml_schema_terms[key] not in schemas_to_include:
                schemas_to_include.append(xml_schema_terms[key])
    
    schemas_string = ' '.join(schemas_to_include)
    rdf_string = "<rdf:RDF " + schemas_string + " >"
    fo = open(PATH, 'w')

    fo.write(xml_schema_terms['header'])
    fo.write(rdf_string)

    for row in metadata_df.index:
        id_string = ''.join(metadata_df['identifier'][row])
        label_string = id_string
        fo.write("<rdf:Description rdf:about='" + id_string + "' rdfs:label='" + label_string + "' >")

        for col in metadata_df.columns:
            if col !='identifier':
                for attr in metadata_df[col][row]:
                    col_string = "<" + col + ">" + str(attr) + "</" + col + ">"
                    fo.write(col_string)

        fo.write("</rdf:Description> \n")

    fo.write("</rdf:RDF>")

    fo.close()

main()

