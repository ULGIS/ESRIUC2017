#-------------------------------------------------------------------------------
# Name:        Reset UT Lands Arcgis Pro Map
# Purpose:     Reset the ArcGIS Pro map to default
#
# Author:      bkennady
#
# Created:     05/04/2016
# Copyright:   (c) bkennady 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
arcpy.env.overwriteOutput

aprx = arcpy.mp.ArcGISProject("CURRENT")
ThreeDMap = aprx.listMaps("3D Map")[0]
UTLMap = aprx.listMaps("UT Lands Map")[0]

# Get layers
LateralLyr = ThreeDMap.listLayers("Oil & Gas Lateral (3D)")[0]
WellPerfsLyr = ThreeDMap.listLayers("Well Perfs (3D)")[0]
LeaseAllDepLyr = ThreeDMap.listLayers("Oil & Gas Lease (All Depths)")[0]
LeaseShallowLyr = ThreeDMap.listLayers("Oil & Gas Lease (Shallow)")[0]
LeaseIntLyr = ThreeDMap.listLayers("Oil & Gas Lease (Intermediate)")[0]
LeaseDeepLyr = ThreeDMap.listLayers("Oil & Gas Lease (Deep)")[0]

WellLyr = ThreeDMap.listLayers("Oil & Gas Well")[0]
LateralTwoDLyr = ThreeDMap.listLayers("Oil & Gas Lateral")[0]
BHLLyr = ThreeDMap.listLayers("Bottom Hole Location")[0]

# Set Query Strings (QS) back to default values
LatQueryString = ""
LeaseAllQS = "ULDB.GIS.ActiveOGLeaseParcel_View.TopDepth = 0 And ULDB.GIS.ActiveOGLeaseParcel_View.BottomDepth = 99999"
LeaseShallowQS = "ULDB.GIS.ActiveOGLeaseParcel_View.TopDepth = 0 And ULDB.GIS.ActiveOGLeaseParcel_View.BottomDepth <> 99999"
LeaseIntQS = "ULDB.GIS.ActiveOGLeaseParcel_View.TopDepth <> 0 And ULDB.GIS.ActiveOGLeaseParcel_View.BottomDepth <> 99999"
LeaseDeepQS = "ULDB.GIS.ActiveOGLeaseParcel_View.TopDepth <> 0 And ULDB.GIS.ActiveOGLeaseParcel_View.BottomDepth = 99999"

TwoDQueryString = "ULDB.GIS.Wellbore_View.WellboreStatusCode IN ('BSW', 'DR', 'GAS', 'GASIW', 'GO', 'LOC', 'NA', 'OIL', 'SI', 'SIG', 'SIGO', 'SIO', 'SIOI', 'SWC', 'SWD', 'SWDG', 'SWDO', 'TA', 'WIW', 'WIWG', 'WIWO', 'WOG', 'WSW') And ULDB.GIS.Wellbore_View.ZoneStatus <> 'NL'"


# Apply query strings to definition query
LateralLyr.definitionQuery = LatQueryString
WellPerfsLyr.definitionQuery = LatQueryString
LeaseAllDepLyr.definitionQuery = LeaseAllQS
LeaseShallowLyr.definitionQuery = LeaseShallowQS
LeaseIntLyr.definitionQuery = LeaseIntQS
LeaseDeepLyr.definitionQuery = LeaseDeepQS
WellLyr.definitionQuery = TwoDQueryString
LateralTwoDLyr.definitionQuery = TwoDQueryString
BHLLyr.definitionQuery = TwoDQueryString

# Turn layers on (Dim the lights, que bad 80s music)
LeaseAllDepLyr.visible = True
LeaseShallowLyr.visible = True
LeaseIntLyr.visible = True
LeaseDeepLyr.visible = True

# Clear Selections
ThreeDMap.clearSelection()
UTLMap.clearSelection()

