
## Overview

The AGS Tools plugin provides three processing algorithms for exporting geotechnical AGS4 data:

| Algorithm | Source | Destination | Purpose |
|-----------|--------|-------------|---------|
| **AGS to DB** (ags_2_db_algorithm.py) | .ags file | GeoPackage / SpatiaLite | Parse and store AGS data in a spatial database |
| **AGS to CSV** (ags_2_csv.py) | .ags file | Folder of .csv files | Export AGS data directly to CSVs for Power BI or other data visualisation tools|
| **DB to CSV** (db_2_csv_algorithm.py) | GeoPackage / SpatiaLite | Folder of .csv files | Export an edited database to CSVs for Power BI |

All three algorithms write a source_file column into every output row, providing a complete audit trail of where data came from. Deduplication uses a prefix-match key on that column to prevent duplicate rows when re-exporting or appending.

---

## The Data Pipeline

### Full End-to-End Flow

```kroki-mermaid
---
config:
  theme: 'forest'
---
graph LR
A([AGS4 file])-->B[[AGS2DB]]
B-->C[(GeoPackage)];
C-->D[[DB2CSV]];
D-->E@{ shape: docs, label: "CSV Folder" };
E-->F(["PowerBI/
Spreadsheet"]);
A-->G[[AGS2CSV]];
G-->F
```

A typical workflow uses **AGS to DB first**, then **DB to CSV** — this allows data to be reviewed and edited in QGIS before being exported to Power BI. The **AGS to CSV** pathway skips the database entirely for quick exports.

---

## The `source_file` Column

Every row in every output CSV contains a `source_file` column. Its format varies by pathway and records full data lineage:

| Pathway | Format | Example |
|---------|--------|---------|
| AGS to CSV | ags_filename\|csv_folder_name\|project_id | Esholt.ags\|site_export\|BH-001 |
| AGS to DB (stored in DB) | ags_filename\|db_filename\|project_id | Esholt.ags\|Esholt.gpkg\|BH-001 |
| DB to CSV (appended) | ags_filename\|db_filename\|project_id\|csv_folder_name | Esholt.ags\|Esholt.gpkg\|BH-001\|site_export |

The `project_id` is read directly from the `PROJ_ID` field in the AGS file's `PROJ` group. If absent, it is omitted from the string.



