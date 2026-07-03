
This guide explains how to use the **AGS Data Visualisation Dashboard** Power BI template created as part of the AGS Toolkit.

The dashboard is designed to help geotechnical engineers quickly view, check and explore AGS data without needing to manually build plots, write queries, or understand the technical structure of Power BI.

!!! warning "Important"

    The dashboard is intended to help users visualise and review AGS data more efficiently.

    It does not replace:

    - Engineering judgement.
    - Formal geotechnical interpretation.
    - Data validation by a competent engineer.
    - Review of the original AGS file where required.

    Users should treat the dashboard as an interactive visual aid for exploring AGS data, identifying trends and checking imported records.

## Recommended Workflow

A typical review workflow is:

1. Open the Power BI template.
2. Enter the CSV folder path.
3. Check the **Project Summary** page.
4. Confirm the correct project and source file are loaded.
5. Check the map and location details.
6. Review which AGS tables contain data.
7. Use the analysis pages to inspect specific test data.
8. Apply filters where needed.
9. Check dynamic units before interpreting charts.
10. Use the tables to verify plotted values where required.


## What the Power BI Dashboard Does

The Power BI dashboard automatically reads the CSV files exported from the AGS Toolkit and turns them into a set of interactive geotechnical plots, maps, tables and summaries.

Each CSV file represents one AGS table, such as `LOCA`, `GEOL`, `SAMP`, `ISPT`, `LLPL`, `TRIT`, `RUCS`, `RPLT`, `RDEN`, `GRAG` or `GRAT`.

Once the CSV folder is loaded, the dashboard automatically:

- Imports the available AGS tables.
- Applies the required data transformations.
- Links related tables together.
- Creates maps, plots and summary tables.
- Reads available units and axis labels from the AGS data where possible.
- Allows the user to filter by project, source file, location type, geological unit and borehole ID.

This means users do not need to manually format AGS tables or create Power BI charts themselves.

## Before Opening the Power BI Dashboard

Before using the Power BI dashboard, the AGS file must first be converted into CSV format using the **AGS to CSV** tool in the QGIS AGS Toolkit.

The converter will create a folder containing multiple CSV files. Each CSV file stores the data from a different AGS group.

For example, the output folder may contain files such as:

- LOCA.csv
- GEOL.csv
- SAMP.csv
- ISPT.csv
- LLPL.csv
- TRIT.csv
- GRAG.csv
- GRAT.csv
- RUCS.csv
- RPLT.csv
- RDEN.csv
- ags_column_metadata.csv
- manifest.csv

Not every AGS file will contain every table. This is normal. For example, a project with no rock testing will not contain useful rock testing records, and the rock testing page may appear empty.

!!! warning "Important"
    Keep all generated CSV files together in the same folder. Do not rename, move, edit or delete individual CSV files before loading the folder into Power BI.

==Screenshot Placeholder – Generated CSV Folder==


==![Generated CSV folder](path/to/screenshot.png)==


## Dashboard Page format

Most pages in the dashboard follow the same basic structure.

There is usually:

- A main chart or map.
- One or more supporting tables.
- Summary cards showing key values.
- Dynamic units and axis labels.
- Filters at the bottom of the page.

The dashboard is interactive. When you apply filters, the charts and tables update automatically.













