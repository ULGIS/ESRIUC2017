# ESRI UC 2017
Python scripts discussed at the ESRI user conference during the summer of 2017.

## Usage
These python scripts show how to:
1. Create 3D feature class laterals in geodatabase from directional surveys
2. Create point along lateral based on measure (m) value
3. Create area of interest tool (AOI) in ArcGIS Pro

# Files
attached file details

## directional_survey_to_lateral.py
Python 2.7

This script uses arcpy to loop through a folder of directional surveys. These directional surveys are in text format of m, z, NS, EW with the start location being 0, 0, 0, 0. The start location for each lateral comes from a well point featureclass. The resulting lateral is then added to a x, y, z, and m enabled line featureclass. An example .txt file has been uploaded.

## create_perfs.py








