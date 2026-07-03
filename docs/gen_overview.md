

This guide summarises the tools and plugins that support AGS visualisation, export, and interpretation in QGIS for engineering users.

## Overview

The workflow around AGS data in QGIS is not usually handled by one single plugin. Instead, different tools support different stages:
- preparing AGS data for mapping
- visualising boreholes and related information
- exporting structured tables for reporting and dashboards
- reviewing geoscience information in a GIS environment

This repo contains one part of that workflow, and external plugins can support the rest.

## 1. AGS CSV Export and Power BI Workflow

This repo provides the AGS processing and export tools used to move data from AGS into a structured format for reporting and dashboard use.

### What These Tools Do

The tools in this repo support:
- AGS to database conversion
- AGS to CSV export
- database to CSV export

This allows a workflow such as:

1. Start with an AGS file.
2. Convert it into a GeoPackage for use in QGIS.
3. Review or edit spatial and tabular data.
4. Export to CSV.
5. Load the CSVs into Power BI.

### Why This Matters for Engineers

This workflow helps teams:
- review borehole and test data spatially
- preserve data lineage through export steps
- standardise tables before reporting
- feed dashboards and repeatable reports

### Repo Tools Included

The main tools available from this repo are:
- `AGS to DB`
- `AGS to CSV`
- `DB to CSV`

These appear in the QGIS Processing Toolbox when the plugin is installed correctly.

### Space for Project-Specific Notes

Add your own notes here about:
- how your team uses the CSV exports
- which tables matter most for reporting
- any naming standards for export folders
- how data is handed over into reporting workflows

## 2. Power BI Template

This section is intentionally left open for your project-specific content.

### Space for Your Input

Add details here about:
- the Power BI template you have created
- how users should connect the exported CSV folder
- which tables are required
- any expected relationships between tables
- any filters, visuals, or dashboard pages already prepared

## 3. QGIS Plotly Graphing Plugin

This is listed as a locally developed or colleague-developed tool for graphing and visualisation inside QGIS.

### Likely Use Cases

Depending on how it has been designed, a Plotly-based graphing plugin may help users:
- plot test values against depth
- create interactive charts from borehole or sample data
- review distributions of results visually
- compare locations or sample groups

### Space for Colleague Input

Add colleague-provided details here about:
- what the plugin is called
- how it is installed
- which datasets it expects
- example chart types it supports
- whether it reads directly from AGS, GeoPackage, or CSV
- any known limitations or recommended workflows

## 4. OpenLog Plugin

OpenLog is an external QGIS plugin that can be used to visualise borehole logs.

### Why It Is Useful

For engineering teams, it can help with:
- viewing borehole log information in a more familiar log-style format
- reviewing sequences down depth
- presenting borehole information visually rather than only in tables

### Typical Role in Workflow

OpenLog is generally useful after spatial data has already been organised in QGIS and you want a borehole-log style presentation layer.

### What Users Should Check

Before relying on it, users should confirm:
- it is compatible with the installed QGIS version
- it supports the fields available in the current dataset
- the borehole structure expected by OpenLog matches the exported or edited data

## 5. Geoscience Plugin

The Geoscience plugin is an external QGIS plugin used more broadly for geological and geoscience visualisation workflows.

### Why It May Be Useful

It may support:
- subsurface interpretation workflows
- geology-focused visualisation
- cross-sections or specialised geological views
- integration of borehole and geology information in a GIS setting

### Typical Role in Workflow

For a geotechnical consultant, this may sit alongside the AGS tools rather than replacing them.

The AGS tools in this repo are mainly about:
- structured conversion
- export
- data handling

The Geoscience plugin may be more useful for:
- interpretation
- review
- communication of geological context

### What Users Should Check

Users should confirm:
- installation method from the QGIS plugin manager
- supported QGIS versions
- whether the plugin expects specific geology fields or layer structures

## Recommended Combined Workflow

One possible workflow for engineering teams is:

1. Use the plugin in this repo to convert AGS into a database or CSV outputs.
2. Use QGIS to review the spatial data and attribute tables.
3. Use OpenLog or another borehole log visualisation plugin when log-style review is needed.
4. Use a Plotly-based plugin where interactive charts help interpret results.
5. Export structured CSVs for Power BI dashboarding.
6. Use the Power BI template for project reporting.

## Notes for Future Expansion

This guide intentionally leaves space for team-specific additions because some tools are internal or locally developed.

Good additions later would include:
- screenshots of each plugin
- installation steps for each plugin
- example workflows by project type
- a comparison table showing when to use each plugin

## Related Documents

- [USER_GUIDE.md](USER_GUIDE.md)
- [QGIS Basics for Geotechnical Engineers](QGIS_BASICS_FOR_GEOTECH_ENGINEERS.md)
- [DATA_FLOW.md](DATA_FLOW.md)
