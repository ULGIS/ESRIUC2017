#-------------------------------------------------------------------------------
# Name:         Find perf locations
# Purpose:      Add perf to geodatabase feature class based on measure distance
#
# Author:       bkennady
# Created:      23/12/2015
#
# Assumptions:  lateral is x, y, z, and m enabled
#               perf is a point feature class that is x, y, z enabled
#               perf and lateral fc are in a projected coordinate system
#               Unique_well_id_name is also in point feature class
#               Tested using enterprise and file geodatabases
#-------------------------------------------------------------------------------
import arcpy
import math

## Variables 
# 3D Lateral Line feature class
laterals = r"N:\foo\bar.gdb\laterals_fc"
perf_fc = r"N:\foo\bar.gdb\perf_point_fc"

# Unique ID for lateral
unique_well_id_name = "BHLID"
unique_well_id = 433

# Measured distance in feet
perf = 12090


# Create empty lists for storing values
loc1 = []
locList = []
# Set location variables surrounding perf
loc1x = 0
loc1y = 0
loc1z = 0
loc1m = 0
loc2x = 0
loc2y = 0
loc2z = 0
loc2m = 10000000000

## Find xyzm locations of the nodes surrounding measure distance value
# Find first node
with arcpy.da.SearchCursor(laterals, ["SHAPE@", "SHAPE@X", "SHAPE@Y", "SHAPE@Z", "SHAPE@M", unique_well_id_name],
                           "", "", True) as cursor:
    for row in cursor:                # 0           1          2          3          4               5
        if row[6] == unique_well_id:
            # Find smallest value surrounding perf location
            print row[5]

            while row[5] > loc1m and row[5] < perf:
                loc1x = row[2]
                loc1y = row[3]
                loc1z = row[4]
                loc1m = row[5]
                # print "loc1m is " + str(loc1m)
                # print "X=" + str(row[2]) + " Y=" + str(row[3]) + " M=" + str(row[4])
del cursor

# Find second node
with arcpy.da.SearchCursor(laterals, ["SHAPE@", "SHAPE@X", "SHAPE@Y", "SHAPE@Z", "SHAPE@M", unique_well_id_name],
                           "", "", True) as cursor:
    for row in cursor:                # 0           1          2          3          4               5
        if row[6] == unique_well_id:
            # Find largest value surrounding perf location
            while row[5] < loc2m and row[5] >= perf:
                loc2x = row[2]
                loc2y = row[3]
                loc2z = row[4]
                loc2m = row[5]
                # print "X=" + str(row[2]) + " Y=" + str(row[3]) + " M=" + str(row[4])
del cursor

# Find xyz of perf located between the two nodes
xv = loc2x - loc1x
yv = loc2y - loc1y
zv = loc2z - loc1z

xyz2 = math.sqrt(xv**2 + yv**2 + zv**2)

xUnitVector = xv/xyz2
yUnitVector = yv/xyz2
zUnitVector = zv/xyz2

DistFromLoc1 = perf - loc1m

# XYZ location of perf
x3 = loc1x + (DistFromLoc1 * xUnitVector)
y3 = loc1y + (DistFromLoc1 * yUnitVector)
z3 = loc1z + (DistFromLoc1 * zUnitVector)

print "x3= " + str(x3)
print "y3= " + str(y3)
print "z3= " + str(z3)

# Create and add to designated feature class
with arcpy.da.InsertCursor(perf_fc, ["Shape@X", "Shape@Y", "Shape@Z", unique_well_id_name]) as cursor:
    cursor.insertRow([x3, y3, z3, unique_well_id])
del cursor
