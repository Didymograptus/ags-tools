The Geopackage created with the ags-tools plugin comprises a spatial table of the LOCA group data and other non-spatial tables that hold the data of all the other groups, e.g. GEOL and ISPT.

The main element of QGIS is the map interface and the ability to select and filter data based on its location. This is fine for the spatial table LOCA because it has co-ordinates and the markers of the the exploratory holes can be presented on the map.

However for AGS groups that don't have co-ordinates e.g. GEOL and ISPT it is not possible to select them via the map. A workaround would be to assign co-ordinates to each row of the table when the GeoPackage is created, however this would create a very cluttered layer tree and map.

The better way to handle non-spatial table is to use the QGIS functionality known as **'Relations'**.

This provides the ability to create relationships between spatial and non-spatial tables using a common data item, which is typically the LOCA_ID.

Once the relations have been created selecting an exploratory hole will also select the data linked by the relationship. This is particularly useful when using the DataPlotly plugin and when filtering or highlighting data using Attribute tables.

!!! note
    In order to use this related data the 'Select by Relationship' plugin must be installed.

The following guidance provides a step by step process of creating and using 'relations' to create a plot of SPT vs depth for a selection of exploratory holes.

