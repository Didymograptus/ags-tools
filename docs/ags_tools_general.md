

## Introduction

This guide provides a practical, step by step workflow for geotechnical engineers and consultants to convert AGS data, build QGIS databases, prepare CSVs for Power BI, and generate geological cross sections.


You will use AGS Tools to:

1. Convert AGS files into a QGIS database for technical checking.
2. Export CSV data for Power BI.
3. Generate geological section outputs for interpretation and communication.

The focus is on what to click, what to check, and what "good" looks like from a geotechnical perspective.

---

## Before You Start - 5-Minute Checklist

1. Install QGIS (recommended: QGIS 3.22 or later).
2. Install and enable AGS Tools.
3. Create a simple folder structure for each project:
   - 01_Raw_AGS
   - 02_QGIS_Database
   - 03_PowerBI_CSV
   - 04_Sections
4. Keep raw AGS files read-only.
5. Confirm project CRS (typically EPSG:27700 in the UK).

==Screenshot Placeholder==

==[Insert screenshot: QGIS download page]==

==[Insert screenshot: QGIS home screen on first launch]==


## Installation/unpacking etc.

Before using any AGS conversion tool, it is worth spending a few minutes making sure the plugin is installed correctly. This prevents frustrating errors later when you are under time pressure.

## Install and enable AGS Tools

1. Open QGIS.
2. From the top menu, click Plugins > Manage and Install Plugins.
3. In the search box, type AGS Tools.
4. Select AGS Tools, then click Install Plugin (or Enable if already installed).
5. Restart QGIS if prompted.

## Confirm the tools are visible in Processing Toolbox

1. Open Processing Toolbox from the right-hand panel.
2. Search for AGS.
3. Confirm these tools appear:
   - AGS2DB
   - AGS2CSV
   - DB2CSV
   - DB to Cross-Sections
   - Summary plots

If these are visible, your installation is ready.

If one or more tools are missing, it is usually a plugin enablement issue rather than a data issue. Re-check installation first before troubleshooting the AGS file.

## If your team provides a ZIP package ?? team??

1. Save the ZIP in a known folder.
2. Unzip fully into a normal folder (do not open and run from inside the ZIP).
3. Keep version names clear, for example AGS_Tools_v1_2.
4. If required by your team process, copy the unpacked plugin folder into your QGIS plugins directory.

## Good practice

- Use one approved plugin version per project issue.
- Avoid combining outputs from different plugin versions in the same final issue pack.

Once this check is complete, you are ready to create your first review database from AGS.

==Screenshot Placeholder==

==[Insert screenshot: Plugins > Manage and Install Plugins window]==

==[Insert screenshot: Processing Toolbox showing AGS tools]==



## Appendix - Plain-language tool summary

- AGS2DB: Converts AGS into a QGIS database for engineering review.
- AGS2CSV: Quick direct export from AGS to CSV.
- DB2CSV: CSV export from reviewed database content.
- DB to Cross-Sections: Generates geological sections from the database.

