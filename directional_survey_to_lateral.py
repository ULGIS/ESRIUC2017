#-------------------------------------------------------------------------------
# Name:         DirectionalSurveyToLateral
# Purpose:      Convert folder of formatted Directional Survey .txt files to
#               lateral feature class
#
# Author:      bkennady
# Created:     16/12/2015
#
# Assumptions:  lateral is x, y, z, and m enabled
#               text file is format m, z, NS, ew
#               text file name is api or unique will id
#               lateral fc is in a projected coordinate system
#               Tested using enterprise and file geodatabases
#-------------------------------------------------------------------------------

import os
import arcpy
import time

# Folder with directional survey text files
inFolder = r"N:\foo\bar\textSurveyFiles"
# Well point feature class, laterals will be shifted to each point location
wellfc = r"foo\bar.sde\well_surface_location"

# Line feature class and field names
lateralfc = r"foo\bar.gdb\lateral_3D"
fields = ['API', 'SHAPE@XY', 'SHAPE@M', 'SHAPE@Z']


date = time.strftime("%Y/%m/%d")

# Check to see if API matches well location in database
if not arcpy.Exists(wellfc):
    print wellcf + "  doesn't exist. Contact GIS Team"

# Create list to hold the all UL well API
WellAPIList = []
invalidAPIList = [] # This list holds API's in the file name that dont match
print "Creating Lists..."

# Create List of UL API's from feature class
with arcpy.da.SearchCursor(wellfc, ["API"]) as cursor:
    for row in cursor:
        if row[0] not in WellAPIList:
            WellAPIList.append(row[0])
del cursor


# check to make sure that file API is valid: Add to given list
validAPIList = []
for x in os.listdir(inFolder):
    if int(x[:-4]) in WellAPIList:
        validAPIList.append(x[:-4])
    if int(x[:-4]) not in WellAPIList:
        invalidAPIList.append(int(x[:-4]))

print validAPIList
print "Lists Created"
for x in os.listdir(inFolder):
    array = arcpy.Array()
    point = arcpy.Point()

    if x[:-4] in validAPIList:
        with arcpy.da.SearchCursor(wellfc, ['API', 'SHAPE@XY']) as cursor:
            for row in cursor:
                GISRow = row[0]
                if GISRow == int(x[:-4]):
                    XStart = row[1][0]
                    YStart = row[1][1]
        del cursor
    f = open(inFolder + "\\" + x)

    for line in f:
        M, Z, NS, EW = line.split()
        point.Z = float(Z) * -1
        point.X = XStart + float(EW)
        point.Y = YStart + float(NS)
        point.M = float(M)
        array.add(point)
        APIsave = str(x[:-4])


    # Create and add polyline to shapefile
    workspace = os.path.dirname(lateralfc)
    edit = arcpy.da.Editor(workspace)
    edit.startEditing()
    edit.startOperation()

    cursor = arcpy.da.InsertCursor(lateralfc, ["SHAPE@", "API", "DateCreated"])
    line = arcpy.Polyline(array, None, True)
    cursor.insertRow([line, APIsave, date])
    del cursor
    array.removeAll()
    f.close()
    print  str(APIsave) + " Lateral Created"
    f.close()

    edit.stopOperation()
    edit.stopEditing(True)

if invalidAPIList == []:
    print ("All files converted")
else:
    print ("These files were not converted")
    print invalidAPIList

