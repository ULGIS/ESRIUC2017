#-------------------------------------------------------------------------------
# Name:        Create AOI in Arcgis Pro 3D Map
# Purpose:     While Running in ArcGIS Pro, takes the laterals selected and
#              filters the layers in scene by passing in a definition query
#
# Author:      bkennady
#
# Created:     05/04/2016
#-------------------------------------------------------------------------------

import arcpy
import sys

arcpy.env.overwriteOutput

# Get Current map and maps
aprx = arcpy.mp.ArcGISProject("CURRENT")
ThreeDMap = aprx.listMaps("3D Map")[0]
UTLMap = aprx.listMaps("UT Lands Map")[0]

# layers from UT Lands Map
UTMLayerLatActive = UTLMap.listLayers("Oil & Gas Lateral")[0]
UTMLayerLatInac = UTLMap.listLayers("Oil & Gas Lateral (Inactive)")[0]

# 3D layers from 3DMap
Lateral3DLyr = ThreeDMap.listLayers("Oil & Gas Lateral (3D)")[0]
LateralTwoDLyr = ThreeDMap.listLayers("Oil & Gas Lateral")[0]
WellPerfsLyr = ThreeDMap.listLayers("Well Perfs (3D)")[0]
LeaseAllDepLyr = ThreeDMap.listLayers("Oil & Gas Lease (All Depths)")[0]
LeaseShallowLyr = ThreeDMap.listLayers("Oil & Gas Lease (Shallow)")[0]
LeaseIntLyr = ThreeDMap.listLayers("Oil & Gas Lease (Intermediate)")[0]
LeaseDeepLyr = ThreeDMap.listLayers("Oil & Gas Lease (Deep)")[0]

# 2D layers from 3D Map
BHLLyr = ThreeDMap.listLayers("Bottom Hole Location")[0]
WellLyr = ThreeDMap.listLayers("Oil & Gas Well")[0]
LateralLyr = ThreeDMap.listLayers("Oil & Gas Lateral")[0]

# Add multipatch Featureclass - Make Feature Layer
Multipatch_fc = r"foo\bar.sde\ULGISv.DBO.MN_LeaseParcel3D"
Multipatch_fl = "MultipatchFL"
arcpy.MakeFeatureLayer_management(Multipatch_fc, Multipatch_fl)


# Unselect any 3D laterals (If there are any, this causes errors when
# selecting in the 3D Map
arcpy.SelectLayerByAttribute_management(Lateral3DLyr, "CLEAR_SELECTION")

# Set up Lateral Query String
LatQueryString = ""

# Get lateral selection set variables
SelecLatCount = 0
SelSetLatAct = UTMLayerLatActive.getSelectionSet()
SelSetLatInac = UTMLayerLatInac.getSelectionSet()
SelSetLatTwoD = LateralTwoDLyr.getSelectionSet()


if str(SelSetLatAct) != "None" or str(SelSetLatInac) != "None":
    LatQueryString = "BHLID IN ("
    try:
        if len(SelSetLatAct):
            rowsLatActive = arcpy.SearchCursor(UTMLayerLatActive)
            for row in rowsLatActive:
                SelecLatCount += 1
                LatQueryString = LatQueryString + str(row.getValue("ULGISv.DBO.MN_Lateral.BHLID")) + ", "
            del rowsLatActive
    except:
        arcpy.AddMessage(arcpy.GetMessages())

    try:
        if len(SelSetLatInac):
            rowsLatInac = arcpy.SearchCursor(UTMLayerLatInac)
            for row in rowsLatInac:
                SelecLatCount += 1
                LatQueryString = LatQueryString + str(row.getValue("ULGISv.DBO.MN_Lateral.BHLID")) + ", "
            del rowsLatInac

    except:
        arcpy.AddMessage(arcpy.GetMessages())


    LatQueryString = LatQueryString[:-2] + ")"
    arcpy.AddMessage("Lat Query string is: " + str(LatQueryString))

elif str(SelSetLatTwoD) != "None":
    LatQueryString = "BHLID IN ("
    rowsLat = arcpy.SearchCursor(LateralTwoDLyr)
    for row in rowsLat:
        SelecLatCount += 1
        LatQueryString = LatQueryString + str(row.getValue("ULGISv.DBO.MN_Lateral.BHLID")) + ", "

    del rowsLat
    LatQueryString = LatQueryString[:-2] + ")"
    arcpy.AddMessage("Lat Query string is: " + str(LatQueryString))


# Set Layer Definition Query and BHL Definition Query
Lateral3DLyr.definitionQuery = LatQueryString
WellPerfsLyr.definitionQuery = LatQueryString

# ---Handle situations of no 3D laterals selected or more than 50 selected------
arcpy.SelectLayerByAttribute_management(Lateral3DLyr, "NEW_SELECTION", LatQueryString )
SelLatCount = arcpy.GetCount_management(Lateral3DLyr)
LatCountNum = int(SelLatCount.getOutput(0))
arcpy.AddMessage("Number of laterals selected" + str(SelLatCount.getOutput(0)))
ThreeDMap.clearSelection()

# Handle if to many laterals are selected
if LatCountNum > 50:
    arcpy.AddMessage("there are to many laterals selected")
    ThreeDMap.clearSelection()
    UTLMap.clearSelection()
    sys.exit

# Handle if no laterals are selected
elif SelecLatCount == 0:
    arcpy.AddMessage("No laterals were selected")
    ThreeDMap.clearSelection()
    UTLMap.clearSelection()
    sys.exit
else:
    # -- Filter feature classes based on selection------------------------------
    # Get Legal Key Set for leases intersecting selected laterals
    # Set up query string variables
    LeaseAllQS = "ULDB.GIS.ActiveOGLeaseParcel_View.TopDepth = 0 And ULDB.GIS.ActiveOGLeaseParcel_View.BottomDepth = 99999"
    LeaseShallowQS = "ULDB.GIS.ActiveOGLeaseParcel_View.TopDepth = 0 And ULDB.GIS.ActiveOGLeaseParcel_View.BottomDepth <> 99999"
    LeaseIntQS = "ULDB.GIS.ActiveOGLeaseParcel_View.TopDepth <> 0 And ULDB.GIS.ActiveOGLeaseParcel_View.BottomDepth <> 99999"
    LeaseDeepQS = "ULDB.GIS.ActiveOGLeaseParcel_View.TopDepth <> 0 And ULDB.GIS.ActiveOGLeaseParcel_View.BottomDepth = 99999"

    # Select laterals then select 3D leases based on selected laterals
    arcpy.SelectLayerByAttribute_management(Lateral3DLyr, "NEW_SELECTION", LatQueryString)
    arcpy.SelectLayerByLocation_management(Multipatch_fl,"INTERSECT_3D", Lateral3DLyr)

    # Get selected leases Legal Keys, create definition query from list
    LegalKeyList = []
    MultipatchCursor = arcpy.SearchCursor(Multipatch_fl)
    for row in MultipatchCursor:
        LegalKeyList.append(str(row.getValue("LegalKey")))

    if len(LegalKeyList):
        LegalKeyQueryString = "ulgisv.SDEDBA.Legal_Layer.LEGAL_KEY IN ("
        for x in LegalKeyList:
            LegalKeyQueryString = LegalKeyQueryString + str(x) + ", "
        LegalKeyQueryString = LegalKeyQueryString[:-2] + ")"

        # Set definition queries to each Lease Layer
        LeaseAllDepLyr.definitionQuery = LegalKeyQueryString + " And " + LeaseAllQS
        LeaseShallowLyr.definitionQuery = LegalKeyQueryString + " And " +  LeaseShallowQS
        LeaseIntLyr.definitionQuery = LegalKeyQueryString + " And " +  LeaseIntQS
        LeaseDeepLyr.definitionQuery = LegalKeyQueryString + " And " +  LeaseDeepQS

    else:
        arcpy.AddMessage("Major Error: No Legal keys found")

    # -- Filter 2D leases on 3D map based on selection---------------------
    # Get API's from selected laterals
    APIList = []
    Lateral3DCursor = arcpy.SearchCursor(Lateral3DLyr, LatQueryString)
    for row in Lateral3DCursor:
        APIList.append(row.getValue("API"))
    # Set up definition query string for 2D layers in 3D map
    APIQueryString = "ULDB.GIS.Wellbore_View.API IN ("
    for API in APIList:
            APIQueryString += str(API) + ", "
    APIQueryString = APIQueryString[:-2] + ")" # + " And " + TwoDQueryString

    # Apply definition queries to 2D layers in 3D Map
    WellLyr.definitionQuery =  APIQueryString
    LateralLyr.definitionQuery = LatQueryString
    BHLLyr.definitionQuery = LatQueryString

    # Clear Selections
    ThreeDMap.clearSelection()
    UTLMap.clearSelection()

del aprx

