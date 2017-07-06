# ESRI UC 2017
Python scripts discussed at the ESRI user conference during the summer of 2017.

## Usage
These python scripts show how to:
1. Create 3D feature class laterals in geodatabase from directional surveys
2. Create point along lateral based on measure (m) value
3. Create area of interest tool (AOI) in ArcGIS Pro

# Files
Details for each script and file

## directional_survey_to_lateral.py
Python 2.x

This script uses arcpy to loop through a folder of directional surveys. These directional surveys are in text format of m, z, NS, EW with the start location being 0, 0, 0, 0. The start location for each lateral comes from a well point feature class. The resulting lateral is then added to a x, y, z, and m enabled line feature class in a geodatabase. An example text file has been uploaded [here](docs/4200349999.txt). The name of the text file is a unique identifier for the well (in this case an API) and used to find the well starting location. Features should be projected in a coordinate system matching the directional survey units. 

## create_perfs.py
Python 2.x

This script adds a point along an m and z enabled line feature class. This point is based on the measure value stored in the m variable. The two points surrounding the measure value are extracted from the line feature class and used to calculate the resulting point. This script assumes that the start of the line is the surface hole location. Each feature class should be projected and have the same unit of measurement.  


## create_AOI.py and reset_AOI.py
Python 3.x

These scripts are used in ArcGIS Pro to create an area of interest tool (AOI). They should be used as guidelines and are not written for easy implementation. They are extremely dependent on the structure of your map and data. 



