# AGS Tools

A QGIS Processing plugin for converting geotechnical AGS4 data into CSV and database formats with complete data lineage tracking.

## What It Does

AGS Tools provides three flexible export pathways to transform AGS4 files for use in Power BI, GIS analysis, and data visualization:

| Pathway | Source | Output | Use Case |
|---------|--------|--------|----------|
| **AGS → CSV** | `.ags` file | CSV folder | Direct export for Power BI or analytics |
| **AGS → Database** | `.ags` file | GeoPackage / SpatiaLite | Store data spatially for QGIS review/editing |
| **Database → CSV** | GeoPackage / SpatiaLite | CSV folder | Export edited database data for analysis |

Each exported row contains a **source_file column** that tracks complete data lineage: which AGS file originated the data, which database it passed through, and which export batch it's in.

## Installation

### 1. Clone or Download This Repository
```bash
git clone <repo-url> c:\YourPath\ags-tools
cd ags-tools
```

### 2. Copy Plugin to QGIS
Copy the entire `ags-tools` folder to your QGIS plugins directory:

**Windows:**
```
C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\ags_tools
```

**macOS:**
```
~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/ags_tools
```

**Linux:**
```
~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/ags_tools
```

### 3. Enable the Plugin in QGIS

1. Open QGIS
2. Go to **Plugins → Manage and Install Plugins**
3. Search for **"AGS Tools"**
4. Click **Install Plugin** (or enable if already installed)
5. Restart QGIS

The plugin now appears in **Processing Toolbox → AGS Tools**

## Requirements

- **QGIS 3.0+** (tested on 3.22+)
- **Python packages:**
  ```
  pandas==3.0.2
  pyproj==3.6.1
  python_ags4==1.2.0
  ```
- **QGIS dependencies:** GDAL/OGR (bundled with QGIS)

Install Python packages:
```bash
pip install -r requirements.txt
```

## Quick Start

### Example 1: Convert AGS to CSV

1. Open **Processing Toolbox → AGS Tools → AGS to CSV**
2. Select your `.ags` file
3. Choose output parent folder
4. Enter a folder name (e.g., `batch_001`)
5. Run

**Output:** Folder containing `samp.csv`, `geol.csv`, etc. + `manifest.csv`

### Example 2: Review Data in QGIS, Then Export

1. **AGS to Database:**
   - Open **Processing Toolbox → AGS Tools → AGS to Database**
   - Generate a `.gpkg` file with point geometries for boreholes
   
2. **Edit in QGIS:**
   - Add new boreholes
   - Modify depths or lithology
   - Adjust coordinates
   
3. **Database to CSV:**
   - Open **Processing Toolbox → AGS Tools → Database to CSV**
   - Export the edited database
   - Full data lineage preserved in `source_file` column

## Key Features

### 1. **Automatic Elevation Calculations**
- Generates `ELEV_<DEPTH_COLUMN>` for every depth measurement
- Formula: `ELEV = Ground_Level - Depth`
- Applies to 45+ AGS groups automatically

### 2. **Complete Data Lineage**
Every row contains a `source_file` column tracking:
```
Example: Esholt.ags|Esholt.gpkg|P001|batch_001

  ↓ Which AGS file originated data
  ↓         ↓ Database it passed through
  ↓         ↓              ↓ Project ID
  ↓         ↓              ↓     ↓ CSV export batch
```

### 3. **Smart Deduplication**
- Re-exporting same AGS file replaces old data (no duplicates)
- Multiple CSV exports from same database tracked separately
- Dedup key: first 3 pipe-parts of `source_file`

### 4. **Append Mode**
- Add new AGS files to existing CSV folders without overwriting
- Deduplication prevents row duplication on re-export
- Ideal for multi-site projects

### 5. **Coordinate Conversion**
- British National Grid (EPSG:27700) → WGS84 (EPSG:4326)
- ~1.1cm precision (7 decimals)
- Automatic geometry creation for borehole locations

### 6. **Manifest Tracking**
Each export creates `manifest.csv` recording:
- Which tables exported, row counts, timestamps
- Complete audit trail of export activity



## Documentation

- **[DATA_FLOW.md](DATA_FLOW.md)** — Complete data flow diagram and pathway explanations
- **[DOCUMENTATION - work in progress.md](DOCUMENTATION%20-%20work%20in%20progress.md)** — Detailed algorithm specifications and deduplication logic

## Testing

Run unit tests:
```bash
python -m pytest test/f
```

## Troubleshooting

### Plugin Not Appearing in Plugins Menu
- Ensure folder is copied to correct QGIS plugins directory (see Installation)
- Restart QGIS after copying
- Check **Plugins → Manage and Install Plugins** → search "AGS Tools" → click Install

### "No module named 'qgis'"
- This is normal; `qgis` is only available inside QGIS
- Run tests/install from within QGIS Python console or with QGIS Python

### Coordinates Not Creating Geometry
- Check for `LOCA_NATE/LOCA_NATN` (BNG) or `LOCA_LAT/LOCA_LON` (WGS84) in your AGS file
- Plugin tries both in priority order; if absent, creates non-spatial tables

### Duplicate Rows After Re-Export
- This shouldn't happen (dedup is automatic)
- Check the `source_file` column — if it's empty or different, dedup won't work
- Ensure AGS2CSV created the file originally (or use DB pathway)

## Performance

- **Small AGS files (< 100KB):** < 5 seconds
- **Medium AGS files (1-5MB):** 10-30 seconds  
- **Large AGS files (> 10MB):** 1-2 minutes

For very large files, consider splitting by site first.

## Contributing

This plugin is actively maintained. For issues, feature requests, or contributions:
- Report bugs with sample AGS file (anonymized if needed)
- Suggest features with use case context
- Pull requests welcome


## Authors

- Oliver Burdekin (burdGIS) — Original author
- Richard Meredith (GeoEnvironmental) — Contributor

- Faith Jamieson - CSV export Contributor 
---

**Questions?** See the detailed documentation files or check the sample workflow in the tests folder.
