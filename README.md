# NCEI Metadatabase
## Constructing a graph database for NCEI metadata

## Overview 

This repository demonstrates the creation of a graph metadatabase using metadata from NCEI's Geoportal (https://www.ncei.noaa.gov/metadata/geoportal/#searchPanel). 
The metadata is collected using a Catalogue Service for the Web (CSW) and converted to Resource Description Framework (RDF) format for import into a graph database.

## How to Use 

### Libraries 

The scripts in this repo use Python 3.7 and a combination of packages listed below. You can download these using `pip install`:
- Beautiful Soup
- KGLab
- RDFLib
- Numpy
- Pandas
- Matplotlib

**NOTE:** An environment package will be posted in future updates to eliminate the need to install multiple packages.

### Visualization 
The graph visualization is demonstrated in `visualization_example.ipynb`. Run this notebook in Jupyter Notebook to visualize a portion of the NCEI metadata graph.

## Planned Updates
- Environment package
