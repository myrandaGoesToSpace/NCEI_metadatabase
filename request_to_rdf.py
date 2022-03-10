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
    gcmd = pd.read_csv("./data/gcmd_science_keywords.csv", index_col=0)

    num_results = 50
    URL = "https://www.ncei.noaa.gov/metadata/geoportal/opensearch?f=csw&start=1000&size=" + str(num_results)
    filename = "data/test_parsed_metadata.xml"

    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "lxml")

    schemas = ['dc:subject', 'dc:title', 'dct:abstract', 'ows:BoundingBox']
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

    # Add GCMD Keywords if applicable
    gcmd_col = []
    for row in metadata_df.index:
        gcmd_row = []
        for s in metadata_df["dc:subject"][row]:
            if s in list(gcmd["label"]):
                gcmd_row.append(str(gcmd[gcmd["label"]==s]["uuid"]).split()[1].strip())
                print("Found keyword: %s" %s)
            else:
                gcmd_row.append("NA")
                print(s)
        gcmd_col.append(gcmd_row)

    metadata_df["gcmd"] = gcmd_col
    print(type(metadata_df["gcmd"][0]))
    print(metadata_df["gcmd"][3])
    print(metadata_df)

    #print(metadata_df[metadata_df["gcmd"]]
    #raise SystemExit(0)

    PATH = filename
    PATH = PATH.replace('xml','csv')

    # Test
    print('path to save:')
    print(PATH)

    metadata_df.to_csv(PATH)

    # Save RDF file

    # Necessary variables
    PATH = filename
    #PATH = PATH.replace('.xml','_rdf.xml')
    PATH = PATH.replace('.xml','.rdf')

    # Dictionary to hold xml schemas
    xml_schema_terms = {}

    xml_schema_terms['header'] = "<?xml version = '1.0' encoding='UTF-8' ?>"
    xml_schema_terms['rdf'] = "xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' "
    xml_schema_terms['dc'] = "xmlns:dc='http://purl.org/dc/elements/1.1/' "
    xml_schema_terms['dct'] = "xmlns:dct='http://purl.org/dc/terms/' "
    xml_schema_terms['dctype'] = "xmlns:dctype='http://purl.org/dc/terms/DCMIType' "
    xml_schema_terms['rdfs'] = "xmlns:rdfs='http://www.w3.org/TR/2014/REC-rdf-schema-20140225/'"
    xml_schema_terms['ows'] = "xmlns:ows='http://www.opengis.net/ows/2.0'"
    xml_schema_terms['gcmd'] = "xmlns:gcmd='https://gcmd.earthdata.nasa.gov/kms/concept/'"

    schemas_to_include = [xml_schema_terms['rdf'], xml_schema_terms['rdfs'], xml_schema_terms['gcmd']]

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
        fo.write("<rdf:type rdf:resource='http://purl.org/dc/terms/DCMIType/Dataset' />")

        for col in metadata_df.columns:
            if col !='identifier' and col != "gcmd":
                for attr in metadata_df[col][row]:
                    col_string = "<" + col + ">" + str(attr).replace('&', '&amp;').strip('\\n').strip('\\t').replace('<', '&lt;').replace('>','&gt;') + "</" + col + ">"
                    fo.write(col_string)
            elif col == "gcmd":
                # add gcmd properties to graph
                # TODO: this currently returns g, c, m, d as keywords - investigate
                gcmd_list = [keyword for keyword in metadata_df[col][row] if keyword != 'NA']
                for g in gcmd_list:
                    gcmd_string = "<dc:subject rdf:resource='https://gcmd.earthdata.nasa.gov/kms/concept/" + str(g) + "' />"
                    fo.write(gcmd_string)



        fo.write("</rdf:Description> \n")

    fo.write("</rdf:RDF>")

    fo.close()

main()

